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
    
    def get(request, tag):
        try:
            supabase_response = supabase.table("users").select("*").eq("user_tag", tag).execute()
            return JsonResponse({"message": "User profile retrieved successfully", "profile": supabase_response.data}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)