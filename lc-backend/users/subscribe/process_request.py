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

@csrf_exempt
def create_checkout_session(request, user_id):
    price_id = 'price_1TPRkPEl7q83Um8U1fYQ4zUY'
    try:
        customer = stripe.Customer.create(
            metadata={"user_id": user_id}
        )

        
        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            subscription_data={
                "metadata": {
                    "user_id": user_id
                }
            },
            mode='subscription',
            success_url='https://launchpad.land/settings',
            cancel_url='https://launchpad.land/settings',
        )

        return JsonResponse({"url": session.url})
    except StripeError as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    except Exception as e:
        # This will expose the real error
        return JsonResponse({"error": str(e)}, status=500)
class process_request:
    
    def post(request, user_id):
        try:
            return create_checkout_session(request, user_id)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)