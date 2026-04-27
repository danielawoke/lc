import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime
import uuid
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
    def post(request, project_id, user_id):
        try:
            data = json.loads(request.body)
            if(data.get("reason") is not None):
                reason = data.get("reason")
                current_rejections = supabase.table("applicants").select("rejection_information").eq("application_id", data.get("application_id")).execute().data[0].get("rejection_information")
                added = False
                # update
                for rejection in current_rejections:
                    if rejection.get("user_id") == user_id:
                        rejection["reason"] = reason
                        added = True
                        break
                # Add normally, this is important
                if not added:
                    current_rejections.append({
                        "user_id": user_id,
                        "reason": reason
                    })

                supabase.table("applicants").update({"rejection_information": current_rejections}).eq("application_id", data.get("application_id")).execute()

            application_info = supabase.table("new_candidates").select("*").eq("application_id", data.get("application_id")).eq("user_id", user_id).eq("project_id", project_id).execute().data
            
            if len(application_info) == 0:
                print("No application")
                return JsonResponse({"error": "No application found"}, status=403)
            
            supabase.table("new_candidates").delete().eq("application_id", data.get("application_id")).eq("user_id", user_id).eq("project_id", project_id).execute()

            return JsonResponse({"message": "Application rejected successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        


# [
#   {
#     "member_id": "djfsa",
#     "configSettings": {
#       "delegated_jobs": [
#         {
#           "job_id": "1321",
#           "delegate_id": "213213"
#         }
#       ],
#       "withdrawn_jobs": [
#         {
#           "job_id": "213213"
#         }
#       ],
#       "withdraw_from_all": true,
#       "reject_remaining_enabled": true
#     }
#   },
#   {
#     "member_id": "69c08fd0db82729c583d",
#     "configSettings": {
#       "delegated_jobs": [
#         {
#           "job_id": "1321",
#           "job_name": "woop",
#           "delegate_id": "213213",
#           "delegate_name": "woop"
#         }
#       ],
#       "withdrawn_jobs": [
#         {
#           "job_id": "213213",
#           "job_name": "woop"
#         }
#       ],
#       "withdraw_from_all": true,
#       "reject_remaining_enabled": true
#     },
#     "delegated_jobs": [],
#     "withdrawn_jobs": [
#       {
#         "job_id": "213213",
#         "job_name": "woop"
#       }
#     ],
#     "reject_remaining": null,
#     "withdraw_from_all": true
#   },
#   {
#     "member_id": "djfsavbn",
#     "configSettings": {
#       "delegated_jobs": [
#         {
#           "job_id": "1321",
#           "delegate_id": "213213"
#         }
#       ],
#       "withdrawn_jobs": [
#         {
#           "job_id": "213213"
#         }
#       ],
#       "withdraw_from_all": true,
#       "reject_remaining_enabled": true
#     }
#   }
# ]