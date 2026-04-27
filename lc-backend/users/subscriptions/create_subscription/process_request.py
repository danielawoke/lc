import django
from django.http import HttpResponse, JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime, timezone
import stripe
from django.views.decorators.csrf import csrf_exempt
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

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(data):

    if data["type"] == "customer.subscription.created":
        user_id = data["data"]["object"]["metadata"]['user_id']
        subscription_id = data["data"]["object"]["id"]
        end_date = data["data"]["object"]["items"]["data"][0]["current_period_end"]
        subscription_end = serialize_datetime(datetime.fromtimestamp(end_date, tz=timezone.utc))
        supabase.table("users").update({"Premium": "Premium", "subscription_id": subscription_id, "subscription_end_date": subscription_end}).eq("user_id", user_id).execute()
    elif data["type"] == "customer.subscription.deleted":
        user_id = data["data"]["object"]["metadata"]['user_id']
        subscription_id = data["data"]["object"]["id"]
        end_date = data["data"]["object"]["items"]["data"][0]["current_period_end"]
        subscription_end = serialize_datetime(datetime.fromtimestamp(end_date, tz=timezone.utc))
        supabase.table("users").update({"Premium": "free", "subscription_id": None, "subscription_end_date": None}).eq("user_id", user_id).execute()
    elif data["type"] == "customer.subscription.updated":
        user_id = data["data"]["object"]["metadata"]['user_id']
        subscription_id = data["data"]["object"]["id"]
        status = data["data"]["object"]["status"]
        end_date = data["data"]["object"]["items"]["data"][0]["current_period_end"]
        subscription_end = serialize_datetime(datetime.fromtimestamp(end_date, tz=timezone.utc))
        if status == "active":
            supabase.table("users").update({"Premium": "Premium", "subscription_id": subscription_id, "subscription_end_date": subscription_end}).eq("user_id", user_id).execute()
        else:
            supabase.table("users").update({"Premium": "marked for deletion", "subscription_id": subscription_id, "subscription_end_date": subscription_end}).eq("user_id", user_id).execute()

    return HttpResponse(status=200)

class process_request:
    
    def post(request):
        try:
            data = json.loads(request.body)
            return stripe_webhook(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        