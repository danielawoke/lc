import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import json
from appwrite.client import Client
from appwrite.services.users import Users
import requests

APPWRITE_ENDPOINT = settings.APPWRITE_ENDPOINT
APPWRITE_PROJECT_ID = settings.APPWRITE_PROJECT_ID
APPWRITE_API_KEY = settings.APPWRITE_API_KEY

ADMIN_EMAIL = settings.ADMIN_EMAIL
ADMIN_PASSWORD = settings.ADMIN_PASSWORD

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


# THis works, but its not best practice. Try to modifiy later if you'd like but I may jsut leave this, at the end when your trying to clean up to code for presentability you can rewrite this
# co piolt said this would be slow since it refreshes constantly, you may want to consider this

client = Client()

client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

users = Users(client)

def check_user_exists(request, user_id):
    try:
        user = users.get(user_id)
        if user is not None:
            print(f"Valid: User with user_id {user_id} exists.")
            return { "response": JsonResponse({"exists": True}), "user": user }
        else:
            print(f"Invalid: User with user_id {user_id} does not exist.")
            return { "response": JsonResponse({"exists": False}), "user": None }

    except Exception as e:
        print(f"Error checking user existence: {str(e)}")
        return { "response": JsonResponse({"error": str(e)}, status=500), "user": None }

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def offerPosition(proposal):
    try:
        project_id = supabase.table("proposals").select("project_id").eq("proposal_id", proposal).execute().data[0].get("project_id")
        application_id = supabase.table("proposal_data").select("application_id").eq("proposal_id", proposal).execute().data[0].get("application_id")
        job_id = supabase.table("applicants").select("job_id").eq("application_id", application_id).execute().data[0].get("job_id")
        application_data = supabase.table("applicants").select("application_object").eq("application_id", application_id).execute().data[0].get("application_object")
        usertag = application_data.get("usertag")
        userid = supabase.table("users").select("user_id").eq("user_tag", usertag).execute().data[0].get("user_id")
        profile_data = supabase.table("users").select("*").eq("user_id", userid).execute().data[0]

        prem = profile_data.get("Premium")
        proj_count = profile_data.get("project_count")

        if proj_count >= 1 and prem == "free":
            return False


        user_info = {
                    "name": profile_data.get("profile_data").get("display_name"),
                    "usertag": usertag,
                    "image": profile_data.get("profile_data").get("UserImage"),
                    "user_id": userid
                }
        members = supabase.table("projects").select("members_info").eq("project_id", project_id).execute().data[0].get("members_info")
        members.append(user_info)
        supabase.table("projects").update({"members_info": members}).eq("project_id", project_id).execute()

        config_settings = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data[0].get("members_config")
        user_config = {
                    "member_id": userid,
                    "configSettings": {
                            "delegated_jobs": [],
                            "withdrawn_jobs": [],
                            "withdraw_from_all": False,
                            "reject_remaining_enabled": False,
                        }
                    }
        config_settings.append(user_config)
        supabase.table("projects").update({"members_config": config_settings}).eq("project_id", project_id).execute()

        

        chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")
        for job in chat_layout.get("Discussions"):

            if job.get("job_id") == job_id:
                i = 0
                while i in range(0, len(job.get("Candidates"))):
                    print(job.get("Candidates")[i])
                    if job.get("Candidates")[i].get("usertag") == usertag:
                        print("found candidate to remove")
                        chatroom = job.get("Candidates")[i]["chat_id"]
                        supabase.table("chat_room_relations").delete().eq("chat_room_id", chatroom).execute()
                        supabase.table("last_message_times").delete().eq("chat_room_id", chatroom).execute()
                        job.get("Candidates").pop(i)
                        break

                    i += 1

        supabase.table("projects").update({"chat_layout": chat_layout}).eq("project_id", project_id).execute()

        return True

    except Exception as e:
        return False

def invite(project_id, user_id):
    try:
        userid = user_id
        usertag = supabase.table("users").select("user_tag").eq("user_id", userid).execute().data[0].get("user_tag")
        profile_data = supabase.table("users").select("*").eq("user_id", userid).execute().data[0]
        

        # prem = profile_data["Premium"]
        # proj_count = profile_data["project_count"]

        # if ((proj_count >= 1) and (prem == "free")):
        #     return False



        user_info = {
                    "name": profile_data.get("profile_data").get("display_name"),
                    "usertag": usertag,
                    "image": profile_data.get("profile_data").get("UserImage"),
                    "user_id": userid
                }
        
        members = supabase.table("projects").select("members_info").eq("project_id", project_id).execute().data[0].get("members_info")
        members.append(user_info)
        supabase.table("projects").update({"members_info": members}).eq("project_id", project_id).execute()

        config_settings = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data[0].get("members_config")
        user_config = {
                    "member_id": userid,
                    "configSettings": {
                            "delegated_jobs": [],
                            "withdrawn_jobs": [],
                            "withdraw_from_all": False,
                            "reject_remaining_enabled": False,
                        }
                    }
        
        config_settings.append(user_config)
        supabase.table("projects").update({"members_config": config_settings}).eq("project_id", project_id).execute()

        return True

    except Exception as e:
        return False

class process_request:
    def post(request, proposal_id):
        try:
            
            data = json.loads(request.body)
            if data["type"] == "offer":
                if(not offerPosition(proposal_id)):
                    return JsonResponse({"message": "fail, not allowed for free"}, status=400)
            else:
                print("a")
                if(not invite(proposal_id, data["user_id"])):
                    return JsonResponse({"message": "fail, not allowed for free"}, status=400)
            
            return JsonResponse({"message": "success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)