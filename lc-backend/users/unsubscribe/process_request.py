import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from stripe import StripeError


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

def cancel_subscription_at_period_end(subscription_id):
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True
    )

class process_request:
    
    def post(request, user_id):
        try:
            subscription_id = supabase.table("users").select("subscription_id").eq("user_id", user_id).execute().data[0]["subscription_id"]
            cancel_subscription_at_period_end(subscription_id)
            supabase.table("users").update({"Premium": "marked for deletion", "subscription_id": subscription_id}).eq("user_id", user_id).execute()
            return JsonResponse({"message": "Subscription cancellation initiated. Your subscription will remain active until the end of the current billing period."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)