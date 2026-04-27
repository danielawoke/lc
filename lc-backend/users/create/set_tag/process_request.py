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


# THis works, but its not best practice. Try to modifiy later if you'd like but I may jsut leave this, at the end when your trying to clean up to code for presentability you can rewrite this
# co piolt said this would be slow since it refreshes constantly, you may want to consider this
def refresh_access_token():
    auth_response = supabase.auth.sign_in_with_password({
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    # session = auth_response.session
    # access_token = session.access_token
    # refresh_token = session.refresh_token



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
        user_id = data.get("user_id")
        user_tag = data.get("user_tag")
        email = data.get("email")
        try:
            response = supabase.table("users").update({
                "user_tag": user_tag,
                "email": email,
            }).eq("user_id", user_id).execute()
            print("Supabase update response:", response)
            return JsonResponse({"message": "User tag updated successfully", "data": response.data}, status=201)
        except Exception as e:
            print(f"Error updating user tag: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)