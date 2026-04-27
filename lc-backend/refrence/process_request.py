import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY
print("Supabase URL:", url)
print("Supabase Key:", key)
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    )
)

def process_request(request, id):
    response = (
        supabase.table("django_migrations")
        .select("*")
        .eq("id", id)
        .execute()
    )

    return JsonResponse({"message": "Request processed successfully!", "data": response.data})
