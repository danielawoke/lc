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


class process_request:
    
    def get(request):
        return JsonResponse({"message": "nothing to see here!"})
    def post(request):
        return JsonResponse({"message": "Request processed successfully!"})
        