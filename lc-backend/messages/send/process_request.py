from urllib import request

import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import json

from django.core.mail import send_mail
from celery import shared_task
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

@shared_task
def send_message_email(messageObjectData):
    
    send_mail(
                subject=f"New message from {messageObjectData['name']}",
                message=f"{messageObjectData['name']}:{messageObjectData['content']}",    
                from_email='notifications@launchpad.land',
                recipient_list=[messageObjectData['email']],
                fail_silently=False,
                html_message=f"""
                    <div style="font-family: Arial;">
                        <h3>{messageObjectData['room']}</h3>
                        <div style='height:400px'; width:400px; background-image: url('{messageObjectData['image']}')/>
                        <h3>{messageObjectData['name']}</h3>
                        <p>{messageObjectData['content']}</p>
                    </div>
                """,
            )
    

class process_request:
    def post(request):
        try:
            message_data = json.loads(request.body)
            supabase_response = supabase.rpc("send_message", {
                    "p_chat_room_id": message_data["chat_room_id"],
                    "p_sender_id": message_data["sender_id"],
                    "p_content": message_data["content"]
                }).execute()
            lastMessage = {
                "user_name": message_data["sender_name"],
                "user_id": message_data["sender_id"],
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
                    user = supabase.table("users").select("notification_settings", 'email').eq("user_id", user_id).execute().data[0]
                    user_settings = user.get('notification_settings')
                    user_email = user.get('email')

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
                    
                    messageObjectData = {
                        "name":message_data["sender_name"],
                        "content": message_data["content"],
                        "room": last_message_clone["title"],
                        "email": user_email,
                        "image": message_data["sender_image"]
                    }    
                    
                    send_message_email.delay(messageObjectData)

            return JsonResponse({"message": "Request processed successfully!", "data": supabase_response.data}, status=201)
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({"error": str(e)}, status=500)