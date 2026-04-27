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
    def get(request, chat_room_id, message_time):
        print(f"Loading messages for chat_room_id: {chat_room_id} after message_time: {message_time}")
        if message_time!="none":
            supabase_response = (
                supabase
                    .from_("messages")
                    .select("*")
                    .eq("chat_room_id", chat_room_id)
                    .lt("time", message_time)
                    .order("time", desc=True)
                    .limit(5)
                    .execute()
            )

        else:
            supabase_response = (
                supabase
                .from_("messages")
                .select("*")
                .eq("chat_room_id", chat_room_id)
                .order("time", desc=True)
                .limit(15)
                .execute()
            )

        supabase_response.data.reverse()
        return JsonResponse(supabase_response.data, safe=False)
    