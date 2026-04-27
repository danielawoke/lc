from urllib import response

import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime

import json
# import psycopg2


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

def decrypt_private_key(encrypted_key):
    # Implement your decryption logic here
    # This is a placeholder function and should be replaced with actual decryption code
    return encrypted_key  # Replace with decrypted key


class process_request:
    def post(request, project_id, user_id):
        if(not request.data.get("private_key") or request.data.get("private_key") != settings.PRIVATE_KEY):
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        supabase_response = (
            supabase
                .from_("projects")
                .select("*")
                .eq("project_id", project_id)
                .execute()
        )

        contained = False

        for member in supabase_response.data[0]['members_info']:
            if member['user_id'] == user_id:
                contained = True
                break
        if contained or supabase_response.data[0].get("is_public"):
            return JsonResponse(supabase_response.data[0], status=200)
        else:
            return JsonResponse({"error": "User does not have access to this project"}, status=403)