import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import json
from appwrite.client import Client
from appwrite.services.users import Users
import requests

APPWRITE_ENDPOINT = settings.APPWRITE_ENDPOINT
APPWRITE_PROJECT_ID = settings.APPWRITE_PROJECT_ID
APPWRITE_API_KEY = settings.APPWRITE_API_KEY

ADMIN_EMAIL = settings.ADMIN_EMAIL
ADMIN_PASSWORD = settings.ADMIN_PASSWORD

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    )
)

client = Client()

client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

users = Users(client)

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

class process_request:
    def get(request):
        return JsonResponse({"message": "test"})
    def post(request):
        data = json.loads(request.body)

        profile_data = {
                "display_name": data["display_name"],
                "UserImage": data["image_url"],
                "location": data["location"],
                "bio": "",
                "bg_color": "rgb(64,0,183)",
                "text_color": "white",
                "links": [],
            }
    
        notification_settings = { 
                "mute_interview_messages": False,  
                "mute_friends_messages": False, 
                "mute_unknown_messages": False, 
                "email_notifications": True 
            } 

    # let profileData = ref(
    #     {
    #         looking_for: "",
    #         user_image: "",
    #         location: "",
    #         skills: [],
    #         links: [],
    #         user_tag: "",
    #         display_name: "",
    #         bio: "",
    #         bg_color: "rgb(64,0,183)",
    #         text_color: "white"
    #     }
    # );
        prem = 'free'
        if len(supabase.table("users").select("*")) <= 1000:
            prem = 'Premium'

        supabase.table("users").update({
                                        "is_verified": True, 
                                        "skills": data["skills"], 
                                        "profile_data": profile_data, 
                                        "looking_for": data["looking_for"], 
                                        "account_configured": True, 
                                        "lng": data["search_coordinates"]['lng'], 
                                        "lat": data["search_coordinates"]['lat'],  
                                        "Premium": prem, 
                                        "people_messaged":[], 
                                        "project_count": 0, 
                                        "notification_settings": notification_settings
                                    }).eq("user_id", data["user_id"]).execute()
        

        
        usertag = supabase.table("users").select("user_tag").eq("user_id", data["user_id"]).execute().data[0].get("user_tag")
        
        supabase.table("search_table").insert({
                                            "type":"person",
                                            "title": data["display_name"], 
                                            "user_id": data["user_id"], 
                                            "looking_for": data.get("looking_for"), 
                                            "public_count": 0,
                                            "remote": True if profile_data.get("location") is '' else False,
                                            "physical": True if profile_data.get("location") is not '' else False,
                                            "lat": data["search_coordinates"]['lat'], 
                                            "lng": data["search_coordinates"]['lng'], 
                                            "location": data["location"],
                                            "image_url": data["image_url"],
                                            "usertag": usertag,
                                            "time_posted": serialize_datetime(datetime.now()),
                                            "skills": data["skills"],
                                        }).execute()

        return JsonResponse({"message": "success"}, status=200)
    