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
    def post(request, job_id):
        try:
            # data = json.loads(request.body)

            supabase_response = (
                supabase
                    .from_("jobs")
                    .delete()
                    .eq("job_id", job_id)
                    .execute()
            )

            supabase.table("search_table").delete().eq("job_id", job_id).execute()

            try:
                project_id = supabase.table("jobs").select("project_id").eq("job_id", job_id).execute().data[0].get("project_id")
                project = supabase.table("projects").select("*").eq("project_id", project_id).execute().data[0]
                i = 0
                while(i < len(project.get("roles"))):
                    if project.get("roles")[i] == job_id:
                        project.get("roles").pop(i)
                        break
                    i += 1

                i = 0
                while i < len(project.get("chat_layout").get("Discussions")):
                    if project.get("chat_layout").get("Discussions")[i].get("job_id") == job_id:
                        project.get("chat_layout").get("Discussions").pop(i)
                        break
                
                full_config = project.get("members_config")

                for config in full_config:
                    i = 0
                    while i < len(config.get("job_id").get("delegated_jobs")):
                        if config.get("job_id").get("delegated_jobs")[i] == job_id:
                            config.get("job_id").get("delegated_jobs").pop(i)
                        else:
                            i += 1
                    i = 0
                    while i < len(config.get("job_id").get("withdrawn_jobs")):
                        if config.get("job_id").get("withdrawn_jobs")[i] == job_id:
                            config.get("job_id").get("withdrawn_jobs").pop(i)
                        else:
                            i += 1

                supabase.table("projects").update({"roles": project.get("roles"), "chat_layout": project.get("chat_layout"), "members_config": full_config}).eq("project_id", project_id).execute()
                supabase.table("applicants").update({"status": "Job deleted"}).eq("job_id", job_id).execute()

            except Exception as e:
                print(f"Error updating project roles and chat layout: {str(e)}")
                

            return JsonResponse(supabase_response.data, safe=False)
        except Exception as e:
            print(f"Error loading jobs: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
