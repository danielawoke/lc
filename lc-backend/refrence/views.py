import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .process_request import process_request
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

class testView(APIView):
    def get(self, request, pk=None):
        return process_request.get(request, id=pk)
    def post(self, request):
        return process_request.post(request)

# class process_request:
#     def get(request, id):
#         if id is None:
#             response = (
#                 supabase.table("django_migrations")
#                 .select("*")
#                 .execute()
#             )
#             return JsonResponse({"message": "Request processed successfully!", "data": response.data})
#         else:
#             response = (
#                 supabase.table("django_migrations")
#                 .select("*")
#                 .eq("id", id)
#                 .execute()
#             )
#             return JsonResponse({"message": "Request processed successfully!", "data": response.data})

#     def post(request):
#         if(request.data.get("tableCreate") == True):
#                 # Raw SQL to create a table
#                 sql = """
#                 Select * from django_migrations;
#                 """
#                 result = supabase.rpc("execute_sql", {"sql": sql}).execute()
#                 return JsonResponse({"message": "Table created successfully!", "data": result.data})
#         else:
#             time = json.dumps(datetime.now(), default=serialize_datetime)
#             response = (
#                 supabase.table("django_migrations")
#                 .insert({"app": "test_app", "name": "test_migration", "applied": time})
#                 .execute()
#             )
#             print("POST request processed:", response.data)
#             return JsonResponse({"message": "Request processed successfully!", "data": response.data})
    

