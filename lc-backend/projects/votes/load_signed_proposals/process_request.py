import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import uuid
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
    def get(request, project_id, user_id):
        try:
            response = supabase.table("proposals").select("*").eq("project_id", project_id).eq("user_id", user_id).eq("voted", True).order("date_added", desc=True).execute()
            return JsonResponse(response.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)