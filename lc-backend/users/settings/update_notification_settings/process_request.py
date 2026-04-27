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
            settings = data.get("setting")
            supabase.table("users").update({"notification_settings": settings}).eq("user_id", user_id).execute()
            return JsonResponse({"message": "Notification settings updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)