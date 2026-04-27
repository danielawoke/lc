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
from django.core.mail import send_mail
from celery import shared_task
import stripe
from django.views.decorators.csrf import csrf_exempt
from stripe import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY


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


    except Exception as e:
        print(str(e))

    return


@shared_task
def send_message_email():
    print("Sending email notification for new message...")
    send_mail(
                subject='Other Message Notification',
                message=f'You have a new messge, check it out here: https://launchpad.land/app/chat/',    
                from_email='notifications@launchpad.land',
                recipient_list=['frozennuts1@gmail.com','dawoke@terpmail.umd.edu'],
                fail_silently=False,
            )


def send(message_data, user_id):
    try:
        supabase_response = supabase.rpc("send_message", {
                "p_chat_room_id": message_data["chat_room_id"],
                "p_sender_id": message_data["sender_id"],
                "p_content": message_data["content"]
            }).execute()
        
        lastMessage = {
            "user_name": "LAUNCHPAD AUTOMATED RESPONSE",
            "user_id": -2,
            "content": message_data["content"],
            "image" : message_data["sender_image"],
            "title": message_data["room_title"] if message_data.get("room_title") else ""
        }

        supabase.from_("last_message_times").update({
                "last_update_time": supabase_response.data['time'], 
                "last_message": lastMessage,
            }).eq("chat_room_id", message_data["chat_room_id"]).execute()
        
        candidate_id = None
        project_title = None

        if message_data.get("project_id") and message_data.get("job_id"):
            project_id = message_data.get("project_id")
            job_id = message_data.get("job_id")
            mainCard = supabase.table("projects").select("project_page").eq("project_id", project_id).execute().data[0].get("project_page").get("_value").get("mainCard")
            job_name = supabase.table("jobs").select("*").eq("job_id", job_id).execute().data[0].get("job_object").get("jobDescription").get("title")[0]
            project_title = mainCard.get("title") + " - " + job_name
            usertag = message_data.get("candidate_usertag")
            candidate_id = supabase.table("users").select("user_id").eq("user_tag", usertag).execute().data[0].get("user_id")

        if project_title is None and message_data.get("project_title"):
            project_title = message_data.get("project_title")

        users = supabase.table("chat_room_relations").select("*").eq("chat_room_id", message_data["chat_room_id"]).execute()

        for user in users.data:
            
            user_id = user.get("user_id")

            if(user.get("notifications_enabled")):

                relation = supabase.table("chat_room_relations").select("relation").eq("user_id", user_id).eq("chat_room_id", message_data["chat_room_id"]).execute().data[0].get("relation")
                user_settings = supabase.table("users").select("notification_settings").eq("user_id", user_id).execute().data[0].get("notification_settings")
                
                if relation == 'interviews' and user_settings.get("mute_interview_messages"):
                    continue
                elif relation == 'friends' and user_settings.get("mute_friends_messages"):
                    continue
                elif relation == 'unknown' and user_settings.get("mute_unknown_messages"):
                    continue

                last_message_clone = lastMessage.copy()
                if project_title is not None:
                    last_message_clone["title"] = project_title + ((" - " + message_data["candidate_name"] ) if ((relation == 'interviewer')) else "")

                if relation == 'interviewer':
                    last_message_clone["job_id"] = message_data.get("job_id")
                    last_message_clone["project_id"] = message_data.get("project_id")

                if message_data.get('interview_project_id') and message_data.get('interview_job_id'):
                    last_message_clone["job_id"] = message_data.get("interview_job_id")
                    last_message_clone["project_id"] = message_data.get("interview_project_id")
                    
                supabase.table("unread_messages").insert({"user_id": user_id, "message_info": last_message_clone, "seen": False, "chat_room_id": message_data["chat_room_id"], "relation": relation}).execute()
                send_message_email.delay()

        return JsonResponse({"message": "Request processed successfully!", "data": supabase_response.data}, status=201)
    except Exception as e:
        print(f"Error occurred: {e}")
        return JsonResponse({"error": str(e)}, status=500)



def cancel_subscription_at_period_end(subscription_id):
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True
    )

class process_request:
    def post(user_id):
        try:
            

            try:
                applications =  supabase.table("applicants").select("*").eq("user_id", user_id).execute()

                for application in applications.data:
                    supabase.table("new_candidates").delete().eq("application_id", application.get("application_id")).execute()
                
                supabase.table("applicants").delete().eq("user_id", user_id).execute()

            except Exception as e:
                print(f"Error deleting from applicants table: {str(e)}")

            try:
                supabase.table("proposals").delete().eq("user_id", user_id).execute()
            except Exception as e:
                print(f"Error deleting from proposals table: {str(e)}")

            try:
                supabase.table("new_candidates").delete().eq("user_id", user_id).execute()
            except Exception as e:
                print(f"Error deleting from new_candidates table: {str(e)}")

            try:
                supabase.table("notifications").delete().eq("user_id", user_id).execute()
            except Exception as e:
                print(f"Error deleting from notifications table: {str(e)}")

            try:
                supabase.table("unread_messages").delete().eq("user_id", user_id).execute()
            except Exception as e:
                print(f"Error deleting from unread_messages table: {str(e)}")

            try:
                for room in supabase.table("chat_room_relations").select("*").eq("user_id", user_id).execute().data:
                    if room.get("relation") == "interviews":
                        data = supabase.table("last_message_times").select("*").eq("chat_room_id", room.get("chat_room_id")).execute().data[0]
                        porject_id = data.get("project_id")
                        job_id = data.get("job_id")
                        chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", porject_id).execute().data[0].get("chat_layout")
                        discussions = chat_layout.get("Discussions")
                        i = 0
                        while i < len(discussions):
                            discussion = discussions[i]
                            print(discussion)
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
                        supabase.table("projects").update({"chat_layout": chat_layout}).eq("project_id", porject_id).execute()
                supabase.table("chat_room_relations").delete().eq("user_id", user_id).execute()
                
            except Exception as e:
                print(f"Error deleting from chat_room_relations table: {str(e)}")
            
            try:
                supabase.table("search_table").delete().eq("user_id", user_id).execute()
            except Exception as e:
                print(f"Error deleting from search_table: {str(e)}")

            try:    
                usertag = supabase.table("users").select("user_tag").eq("user_id", user_id).execute().data[0].get("user_tag")
                projects = supabase.rpc("get_projects_by_member_json",{"tag": usertag}).execute()
                for project in projects.data:
                    remove_memeber(user_id, project.get("project_id"))
                    print(f"Error removing member from project {project.get('project_id')}: {str(e)}")
            except Exception as e:
                print(f"Error occurred while fetching projects: {str(e)}")

            try:
                stripeID = supabase.table('users').select('subscription_id').eq('user_id',user_id).execute().data[0]
                if stripeID != None:
                    cancel_subscription_at_period_end(stripeID)
            except Exception as e:
                print(f"Error ending subscription: {str(e)}")

            try: 
                users.delete(user_id)
                supabase.table("users").delete().eq("user_id", user_id).execute()
            except Exception as e:
                print(f"Error deleting user from Appwrite or Supabase: {str(e)}")
            
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
        