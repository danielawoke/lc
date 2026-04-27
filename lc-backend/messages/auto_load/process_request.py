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
    def get(request, user_id, receiver_tag):
        supabase_response = (
            supabase.table("chat_room_relations")
            .select("chat_room_id")
            .eq("user_id", user_id)
            .eq("usertag", receiver_tag)
            .execute()
        )
        return JsonResponse(supabase_response.data, safe=False)
    