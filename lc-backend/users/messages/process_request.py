import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime

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
    def get(request, user_id, relation):
        try:
            print(relation, user_id)
            supabase_response = supabase.rpc("get_user_chatrooms", {"p_user_id": user_id, "p_relation": relation}).execute()
            print("Chat rooms fetched from Supabase:", supabase_response.data)
            return JsonResponse({"message": "User created successfully", "chatrooms": supabase_response.data}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)})