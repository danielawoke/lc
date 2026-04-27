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


def check_delegate_cycles(project_config_settings, first_list_of_delegated_jobs):
    config_dict = {config.get("member_id"): config.get("configSettings").get("delegated_jobs") for config in project_config_settings}
    print(config_dict)
    for job in first_list_of_delegated_jobs:
        job_id = job.get("job_id")
        delegate_id = job.get("delegate_id")
        visited = set()
        current_delegate_id = delegate_id

        while current_delegate_id is not None:
            if current_delegate_id in visited:
                return True
            visited.add(current_delegate_id)

            delegated_jobs = config_dict.get(current_delegate_id, [])
            next_delegate = None
            for job in delegated_jobs:
                if job.get("job_id") == job_id:
                    next_delegate = job.get("delegate_id")
                    break

            if next_delegate is None:
                break
            current_delegate_id = next_delegate
    return False

class process_request:
    def post(request, project_id, user_id):
        try:
            response = supabase.table("projects").select("members_config").eq("project_id", project_id).execute()
            request_data = json.loads(request.body)
            configSettings = request_data.get("config_settings")
            first_list_of_delegated_jobs = configSettings.get("delegated_jobs")
            for config in response.data[0].get("members_config"):
                if config.get("member_id") == user_id:
                    config["configSettings"]["withdraw_from_all"] = configSettings.get("withdraw_from_all")
                    config["configSettings"]["reject_remaining_enabled"] = configSettings.get("reject_remaining_enabled")
                    config["configSettings"]["delegated_jobs"] = configSettings.get("delegated_jobs")
                    config["configSettings"]["withdrawn_jobs"] = configSettings.get("withdrawn_jobs")

            if check_delegate_cycles(response.data[0].get("members_config"), first_list_of_delegated_jobs):
                return JsonResponse({"error": "Delegate cycle detected"}, status=400)

            update_response = supabase.table("projects").update({"members_config": response.data[0].get("members_config")}).eq("project_id", project_id).execute()
            return JsonResponse(update_response.data, safe=False)
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