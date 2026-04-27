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
    def get(request, user_id, friend_id):
        try:
            print(f"Checking if user_id: {user_id} and friend_id: {friend_id} are friends.")
            supabase_response = supabase.table("friends").select("*").eq("user_id", user_id).eq("friend_id", friend_id).execute()
            is_friend = len(supabase_response.data) > 0
            return JsonResponse({"is_friend": is_friend}, status=200)
        except Exception as e:
            print(f"Error checking friendship: {str(e)}")
            return JsonResponse({"error": "Failed to check friendship"}, status=500)
