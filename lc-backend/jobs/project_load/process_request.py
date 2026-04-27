import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import time
import schedule
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
    def get(request, project_id, view_mode):
        print(f"Loading jobs for project_id: {project_id}")
        try:
            if(view_mode == "false"):
                supabase_response = (
                    supabase
                        .from_("jobs")
                        .select("*")
                        .eq("project_id", project_id)
                        .execute()
                )
            else:
                supabase_response = (
                    supabase
                        .from_("jobs")
                        .select("*")
                        .eq("project_id", project_id)
                        .eq("closed", False)
                        .execute()
                )

            return JsonResponse(supabase_response.data, safe=False)
        except Exception as e:
            print(f"Error loading jobs: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
        