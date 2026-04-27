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
        # Query the "users" collection where "user_id" field equals the given user_id
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

class process_request:
    def post(user_id, application_id):
        try:
            job_id = supabase.table("applicants").select("job_id").eq("application_id", application_id).execute().data[0].get("job_id")
            project_id = supabase.table("jobs").select("project_id").eq("job_id", job_id).execute().data[0].get("project_id")
            try:
                for room in supabase.table("chat_room_relations").select("*").eq("user_id", user_id).execute().data:
                    if room.get("relation") == "interviews":
                        data = supabase.table("last_message_times").select("*").eq("chat_room_id", room.get("chat_room_id")).execute().data[0]
                        chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")
                        discussions = chat_layout.get("Discussions")
                        i = 0
                        while i < len(discussions):
                            discussion = discussions[i]
                            if discussion.get("job_id") == job_id:
                                candidates = discussion.get("Candidates")
                                j = 0
                                while j < len(candidates):
                                    candidate = candidates[j]
                                    if candidate.get("user_id") == user_id:
                                        candidates.pop(j)
                                        break
                                    j += 1
                                break
                            i += 1
                        chat_layout["Discussions"] = discussions
                        supabase.table("projects").update({"chat_layout": chat_layout}).eq("project_id", project_id).execute()
                supabase.table("chat_room_relations").delete().eq("user_id", user_id).execute()
                
            except Exception as e:
                print(f"Error deleting from chat_room_relations table: {str(e)}")

            supabase.table("applicants").delete().eq("application_id", application_id).eq("user_id", user_id).execute()
            proposals = supabase.table("proposal_data").select("proposal_id").eq("application_id", application_id).execute().data
            for proposal in proposals:
                supabase.table("proposals").delete().eq("proposal_id", proposal.get("proposal_id")).execute()
            supabase.table("proposal_data").delete().eq("application_id", application_id).execute()
            supabase.table("applicants").delete().eq("application_id", application_id).execute()
            supabase.table("new_candidates").delete().eq("application_id", application_id).execute()

            
            
            return JsonResponse({"message": "Application deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)