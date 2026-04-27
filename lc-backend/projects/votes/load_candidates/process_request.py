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
            job_list = supabase.table("projects").select("*").eq("project_id", project_id).execute().data[0]
            jobs = job_list.get("roles")
            config = job_list.get("members_config")
            user_config = None
            for config_option in config:
                if config_option.get("member_id") == user_id:
                    user_config = config_option
                    break

            full_applicant_listing = []
            for job in jobs:
                 
                if not any(j.get("job_id") == job for j in user_config.get("configSettings").get("delegated_jobs")) and not any(j.get("job_id") == job for j in user_config.get("configSettings").get("withdrawn_jobs")):
                    user_config["job_id"] = job
                    job_obj = supabase.table("jobs").select("*").eq("job_id", job).execute().data[0]
                    applicant_listing = {
                        "job_id": job,
                        "job_title": job_obj.get("job_object").get("jobDescription").get("title")[0],
                    }
                    applicant_listing["candidates"] = supabase.table("new_candidates").select("*").eq("project_id", project_id).eq("job_id", job).eq("user_id", user_id).execute().data
                    full_applicant_listing.append(applicant_listing)

            return JsonResponse({"candidates": full_applicant_listing}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)