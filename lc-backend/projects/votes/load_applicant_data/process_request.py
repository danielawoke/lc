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
    def get(request, applicant_id):
        try:
            applicant_data = supabase.table("applicants").select("*").eq("application_id", applicant_id).execute().data
            return JsonResponse({"applicant_data": applicant_data[0]}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)