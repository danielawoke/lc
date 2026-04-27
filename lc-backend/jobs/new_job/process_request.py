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
import uuid
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


def create_unique_job_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("jobs").select("job_id").eq("job_id", new_id).execute()
        if len(response.data) == 0:
            return new_id


class process_request:
    def post(request, project_id):
        try:
            data = json.loads(request.body)
            job_id = create_unique_job_UUID()
            job_object = data.get("job_object")
            supabase_response = (
                supabase
                    .from_("jobs")
                    .insert({"job_object": job_object, "project_id": project_id, "closed": job_object.get("settings").get("closed")[0], "job_id": job_id})
                    .execute()
            )
                
            project = supabase.table("projects").select("*").eq("project_id", project_id).execute().data[0]
            project.get("roles").append(job_id)
            project.get("chat_layout").get("Discussions").append({
                "Job":job_object.get("jobDescription").get("title")[0],
                "job_id": job_id,
                "Candidates":[]
            })
            supabase.table("projects").update({"roles": project.get("roles"), "chat_layout": project.get("chat_layout")}).eq("project_id", project_id).execute()

            supabase.table("search_table").insert({
                "job_id":job_id,
                "project_id": project_id,
                "type": "job",
                "lat": project.get("project_page").get("_value").get("mainCard").get("coordinates").get("lat"),
                "lng": project.get("project_page").get("_value").get("mainCard").get("coordinates").get("lng"),
                "physical": not project.get("project_page").get("_value").get("mainCard").get("physicalLocation"),
                "remote": project.get("project_page").get("_value").get("mainCard").get("remote"),
                "location": project.get("project_page").get("_value").get("mainCard").get("location"),
                "title": job_object.get("jobDescription").get("title")[0],
                "description": job_object.get("jobDescription").get("summary")[0],
                "time_posted": serialize_datetime(datetime.now())
            }).execute()

            return JsonResponse(supabase_response.data, safe=False)

        except Exception as e:
            print(f"Error loading jobs: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
        