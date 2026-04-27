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

def remove_memeber(user_id, project_id):
    try:
        
        members = supabase.table("projects").select("members_info").eq("project_id", project_id).execute().data[0].get("members_info")
        members = [member for member in members if member.get("user_id") != user_id]
        supabase.table("projects").update({"members_info": members}).eq("project_id", project_id).execute()

        config_settings = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data[0].get("members_config")
        config_settings = [config for config in config_settings if config.get("member_id") != user_id]
        supabase.table("projects").update({"members_config": config_settings}).eq("project_id", project_id).execute()

        supabase.table("proposals").delete().eq('user_id', user_id ).eq("project_id", project_id).execute()
        supabase.table("new_candidates").delete().eq('user_id', user_id ).eq("project_id", project_id).execute()

        count = supabase.table("users").select("project_count").eq("user_id", user_id).execute().data[0].get("project_count")
        supabase.table("users").update({"project_count", count - 1}).eq("user_id", user_id).execute()

    except Exception as e:
        print(str(e))
    return


def delete_project(project_id):
    try:
        jobs = supabase.table("jobs").select("job_id").eq("project_id", project_id).execute().data
        for job in jobs:
            applications = supabase.table("applicants").select("*").eq("job_id", job.get("job_id")).execute().data
            for application in applications:
                supabase.table("applicants").update({"status": "Project Deleted"}).eq("application_id", application.get("application_id")).execute()
            supabase.table("jobs").delete().eq("job_id", job.get("job_id")).execute()

        supabase.table("proposal_data").delete().eq("project_id", project_id).execute()
        # delete all proposal data to

        chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")
        chatRoomIds = []
        for chat in chat_layout.get("Genearl"):
            chatRoomIds.append(chat.get("chat_id"))

        for job in chat_layout.get("Discussions"):
            for chat in job.get("Candidates"):
                chatRoomIds.append(chat.get("chat_id"))

        for chatRoomId in chatRoomIds:
            supabase.table("chat_room_relations").delete().eq("chat_room_id", chatRoomId).execute()
            supabase.table("last_message_times").delete().eq("chat_room_id", chatRoomId).execute()

        supabase.table("projects").delete().eq("project_id", project_id).execute()

    except Exception as e:
        print(str(e))
    return

class process_request:
    def post(project_id, user_id):
        try:
            remove_memeber(user_id, project_id)
            length = len(supabase.table("projects").select("members_info").eq("project_id", project_id).execute().data[0].get("members_info"))
            print(length)
            if length == 0:
                delete_project(project_id)
            return JsonResponse({"message": "User removed from project successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
