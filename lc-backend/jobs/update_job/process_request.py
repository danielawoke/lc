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
    def post(request, project_id, job_id):
        try:
            data = json.loads(request.body)
            job_object = data.get("job_object")
            supabase_response = (
                supabase
                    .from_("jobs")
                    .update({"job_object": job_object, "project_id": project_id, "job_id": job_id, "closed": job_object.get("settings").get("closed")[0]})
                    .eq("job_id", job_id)
                    .execute()
            )
            if len(supabase_response.data) == 0:
                supabase_response = (
                    supabase
                        .from_("jobs")
                        .insert({"job_object": job_object, "project_id": project_id, "job_id": job_id, "closed": job_object.get("settings").get("closed")[0]})
                        .execute()
                )

            project_page = supabase.table("projects").select("*").eq("project_id", project_id).execute().data[0]
            print("a")
            if not job_object.get("settings").get("closed")[0]:
                print("a")
                if supabase.table("search_table").select("*").eq("job_id", job_id).execute().data:
                    print("a")
                    supabase.table("search_table").update({
                        "lat": project_page.get("project_page").get("_value").get("mainCard").get("coordinates").get("lat"),
                        "lng": project_page.get("project_page").get("_value").get("mainCard").get("coordinates").get("lng"),
                        "physical": not project_page.get("project_page").get("_value").get("mainCard").get("physicalLocation"),
                        "remote": project_page.get("project_page").get("_value").get("mainCard").get("remote"),
                        "location": project_page.get("project_page").get("_value").get("mainCard").get("location"),
                        "title": job_object.get("jobDescription").get("title")[0],
                        "description": job_object.get("jobDescription").get("summary")[0],
                    }).eq("job_id", job_id).execute()
                else:
                    print("b")
                    supabase.table("search_table").insert({
                        "job_id":job_id,
                        "project_id": project_id,
                        "type": "job",
                        "lat": project_page.get("project_page").get("_value").get("mainCard").get("coordinates").get("lat"),
                        "lng": project_page.get("project_page").get("_value").get("mainCard").get("coordinates").get("lng"),
                        "physical": not project_page.get("project_page").get("_value").get("mainCard").get("physicalLocation"),
                        "remote": project_page.get("project_page").get("_value").get("mainCard").get("remote"),
                        "location": project_page.get("project_page").get("_value").get("mainCard").get("location"),
                        "title": job_object.get("jobDescription").get("title")[0],
                        "description": job_object.get("jobDescription").get("summary")[0],
                        "time_posted": serialize_datetime(datetime.now())
                    }).execute()
            else:
                print("b")
                supabase.table("search_table").delete().eq("job_id", job_id).execute()

            return JsonResponse(supabase_response.data, safe=False)
        except Exception as e:
            print(f"Error loading jobs: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
        