import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime

import json
# import psycopg2

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

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

class process_request:
    
    def post(request, user_id):
        try:
            data = json.loads(request.body)
            supabase.table("users").update({"looking_for": data.get("looking_for"), "profile_data": data.get("profile_data"), "lat": data.get("lat"), "lng": data.get("lng")}).eq("user_id", user_id).execute()
            try:

                full_user_profile = supabase.table("users").select("*").eq("user_id", user_id).execute().data[0]
                
                if supabase.table("search_table").select("*").eq("user_id", user_id).execute().data:
                    supabase.table("search_table").update({
                                                        "type":"person",
                                                        "title": data.get("profile_data").get("display_name"), 
                                                        "user_id": user_id, 
                                                        "looking_for": data.get("looking_for"), 
                                                        "public_count": 0,
                                                        "remote": True if data.get("profile_data").get("location") == '' else False,
                                                        "physical": True if data.get("profile_data").get("location") != '' else False,
                                                        "lat": data.get("lat"), 
                                                        "lng": data.get("lng"), 
                                                        "location": data.get("profile_data").get("location"), 
                                                        "image_url": data.get("profile_data").get("UserImage"),
                                                        "usertag": full_user_profile.get("user_tag"),
                                                        "time_posted": serialize_datetime(datetime.now()),
                                                        "skills": full_user_profile.get("skills"),
                                                    }).eq("user_id", user_id).execute()
                    
                else:
                    supabase.table("search_table").insert({
                                                        "type":"person",
                                                        "title": data.get("profile_data").get("display_name"), 
                                                        "user_id": user_id, 
                                                        "looking_for": data.get("looking_for"), 
                                                        "public_count": 0,
                                                        "remote": True if data.get("profile_data").get("location") == '' else False,
                                                        "physical": True if data.get("profile_data").get("location") != '' else False,
                                                        "lat": data.get("lat"), 
                                                        "lng": data.get("lng"), 
                                                        "location": data.get("profile_data").get("location"), 
                                                        "image_url": data.get("profile_data").get("UserImage"),
                                                        "usertag": full_user_profile.get("user_tag"),
                                                        "time_posted": serialize_datetime(datetime.now()),
                                                        "skills": full_user_profile.get("skills"),
                                                    }).execute()
            except Exception as e:
                print("Error inserting into search_table:", str(e))
            return JsonResponse({"message": "Personal settings updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)