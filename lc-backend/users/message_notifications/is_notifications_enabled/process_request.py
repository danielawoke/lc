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

client = Client()

client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

users = Users(client)

class process_request:
    def get(user_id, chat_room_id):
        try:
            relation = supabase.table("chat_room_relations").select("*").eq("user_id", user_id).eq("chat_room_id", chat_room_id).execute().data
            if len(relation) > 0:
                notifications_enabled = relation[0].get("notifications_enabled", False)
                return JsonResponse({"status": True}, status=200)
            else:
                return JsonResponse({"status": False}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
