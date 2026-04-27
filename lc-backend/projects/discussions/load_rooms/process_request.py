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

# let mainCardData = ref({
#     title: "Project Title",
#     location: "The location they game",
#     image: new URL("@/assets/founder-space/edit/default-comp-image.png", import.meta.url),
#     color: {backgroundColor: "white", titleColor: "#000000", contentColor: "#000000", locationColor: "#000000"},
#     physicalLocation:false,
#     remote:true,
#     content: `<pre id='desc-text'>Welcome to your project draft! \n\nThis is the fouders's space of your project, it is where you will manage candidates that apply to your project, talk to and interview new candidates, design your project page, and the create role postings to recruit more memebers.\n\nTo set up your project page, click the pencil edit icon to the bottom right to make changes. Text editors will pop up in corresponding locations, and the rest should be easy to follow!\n\nTo add roles/job postions for your project, edit the jobs card underneath this one to add roles. Simply click on edit, and in the list of jobs you select the \"ADD ROLE\" button and a job creation menu will come up with more details.\n\nWhen new candidates apply, your entire team will be able to review thier application through the \"votes\" tab to the right, and collectively vote to reject or proceed to with a discussion/interview in the \"chat\"  tab in the right menu. For more details, go to the \"help\" tab.\n\nIf you feel like your project needs more space to really be presented propperly, at the bottom you can add extra cards by clicking the \"ADD CARD\" button.\n\nWhen youre ready to publish your project, go to settings, add a project descritpion, thne detoggle the \"Privatize\" setting under publicity.\n\nHave fun making something awsome, and I deeply thank you for contributing to lauch pad's community </pre>`
# });


def create_unique_project_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("projects").select("project_id").eq("project_id", new_id).execute()
        if len(response.data) == 0:
            return new_id

def create_unique_job_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("jobs").select("job_id").eq("job_id", new_id).execute()
        if len(response.data) == 0:
            return new_id


class process_request:
    def get(request, project_id):
        try:
            response = supabase.table("projects").select("*").eq("project_id", project_id).execute().data[0].get("chat_layout")
            return JsonResponse(response, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)