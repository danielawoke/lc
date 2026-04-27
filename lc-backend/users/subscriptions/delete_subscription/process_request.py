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
    
    def post(request, user_id):
        try:
            data = json.loads(request.body)
            if not user_id:
                return JsonResponse({"error": "user_id is required"}, status=400)
            print("parsing")
            jsonData = {
                "UserImage": data.get("user_image", ""),
                "location": data.get("location", ""),
                "display_name": data.get("display_name", ""),
                "links": data.get("links", []),
                "bio": data.get("bio", ""),
                "bg_color": data.get("bg_color", ""),
                "text_color": data.get("text_color", "")
            }
            print("JSON Data:", jsonData)
            supabase.from_("users").update({"profile_data": jsonData, "skills": data.get("skills")}).eq("user_id", user_id).execute()
            supabase.table("search_table").update({"skills": data.get("skills")}).eq("user_id", user_id).execute()
            return JsonResponse({"message": "User profile updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)