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


def find_unique_room_id():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("chat_room_relations").select("chat_room_id").eq("chat_room_id", new_id).execute()
        if len(response.data) == 0:
            return new_id


class process_request:
    def post(request):

        room_id = find_unique_room_id()

        data = json.loads(request.body)
        print(data.get("type"))
        if data.get("type") == "personal":
            try:
                person1 = data.get("users")[0]
                
                now = (datetime.utcnow())
                users = supabase.table("users").select("*").eq("user_id", person1.get("user_id")).execute().data[0]
                people_messaged = users.get('people_messaged')
                people_messaged.append(serialize_datetime(now))
                supabase.table("users").update({"people_messaged":people_messaged}).eq("user_id",person1.get("user_id")).execute()

                person2 = data.get("users")[1]
                supabase.table("chat_room_relations").insert({"chat_room_id": room_id, "user_id": person1.get("user_id"), "relation": data.get("relation")[0],"room_name": person2.get("profile_data").get("display_name"), "room_image": person2.get("profile_data").get("UserImage"), "usertag": person2.get("user_tag")}).execute()
                supabase.table("chat_room_relations").insert({"chat_room_id": room_id, "user_id": person2.get("user_id"), "relation": data.get("relation")[1], "room_name": person1.get("profile_data").get("display_name"), "room_image": person1.get("profile_data").get("UserImage"), "usertag": person1.get("user_tag")}).execute()
                supabase.table("last_message_times").insert({"chat_room_id": room_id}).execute()
                
                return JsonResponse({"message": "Chat room created successfully", "chat_room_id": room_id}, status=201)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
            
        elif data.get("type") == "interview":
            return JsonResponse({"error": "TODO for interviews."}, status=400)
        
        else:
            return JsonResponse({"error": "Invalid chat room type"}, status=400)