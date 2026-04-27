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
    def get(self, user_id, project_id):
        try:
            all_configs_and_jobs = supabase.table("projects").select("members_config", "roles").eq("project_id", project_id).execute().data[0]
            all_configs = all_configs_and_jobs.get("members_config")
            userConfig = None
            job_ids = all_configs_and_jobs.get("roles")
            jobs = []
            users = []
            for config in all_configs:
                # add anonyimity to config for quicker access when implemented
                if config.get("member_id") == user_id:
                    userConfig = config
                else: 
                    user_data = supabase.table("users").select("*").eq("user_id", config.get("member_id")).execute().data
                    if len(user_data) > 0:
                        users.append(user_data[0])

            for job_id in job_ids:
                job = supabase.table("jobs").select("*").eq("job_id", job_id).execute().data[0]
                jobs.append(job)

            return JsonResponse({"config_settings": userConfig, "jobs": jobs, "members": users}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        