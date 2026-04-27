import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime, timezone
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

def create_unique_room_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("messages").select("chat_room_id").eq("chat_room_id", new_id).execute()
        if len(response.data) == 0:
            return new_id

class process_request:
    def post(request, project_id):
        try:
            request_data = json.loads(request.body)
            room_id = request_data.get("chatroomID")
            # job_id = request_data.get("jobID")
            layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")
            for room in layout.get("Genearl"):
                if room.get("chat_id") == room_id:
                    room["name"] = request_data.get("newName")

            supabase.table("projects").update({"chat_layout": layout}).eq("project_id", project_id).execute()

            return JsonResponse({"message": "Chat room name updated successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

