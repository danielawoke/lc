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
    def post(entry_id):
        try:
            # print(f"Incrementing public count for entry_id: {entry_id}")

            new_count_response = supabase.table("search_table").select("public_count").eq("id", entry_id).execute()

            if len(new_count_response.data) == 0:
                return JsonResponse({"error": "Entry not found"}, status=404)
            
            supabase.table("search_table").update({"public_count": new_count_response.data[0].get("public_count", 0) + 1}).eq("id", entry_id).execute()
            
            return JsonResponse({"message": "Public count incremented successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)