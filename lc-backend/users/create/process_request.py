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

class process_request:
    def get(request):
        return JsonResponse({"message": "test"})
    def post(request):
        data = json.loads(request.body)
        user_id = data.get("id")
        check_user_exists_response = check_user_exists(request, user_id)

        if check_user_exists_response["response"].status_code != 200:
            return check_user_exists_response
        user = check_user_exists_response["user"]
        
        email_verified = user.emailverification
        
        try:
            response = supabase.table("users").insert({
                "user_id": user_id,
                "is_verified": email_verified
            }).execute()
            return JsonResponse({"message": "User created successfully", "data": response.data}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)})