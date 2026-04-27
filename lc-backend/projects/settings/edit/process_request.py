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

# let mainCardData = ref({
#     title: "Project Title",
#     location: "The location they game",
#     image: new URL("@/assets/founder-space/edit/default-comp-image.png", import.meta.url),
#     color: {backgroundColor: "white", titleColor: "#000000", contentColor: "#000000", locationColor: "#000000"},
#     physicalLocation:false,
#     remote:true,
#     content: `<pre id='desc-text'>Welcome to your project draft! \n\nThis is the fouders's space of your project, it is where you will manage candidates that apply to your project, talk to and interview new candidates, design your project page, and the create role postings to recruit more memebers.\n\nTo set up your project page, click the pencil edit icon to the bottom right to make changes. Text editors will pop up in corresponding locations, and the rest should be easy to follow!\n\nTo add roles/job postions for your project, edit the jobs card underneath this one to add roles. Simply click on edit, and in the list of jobs you select the \"ADD ROLE\" button and a job creation menu will come up with more details.\n\nWhen new candidates apply, your entire team will be able to review thier application through the \"votes\" tab to the right, and collectively vote to reject or proceed to with a discussion/interview in the \"chat\"  tab in the right menu. For more details, go to the \"help\" tab.\n\nIf you feel like your project needs more space to really be presented propperly, at the bottom you can add extra cards by clicking the \"ADD CARD\" button.\n\nWhen youre ready to publish your project, go to settings, add a project descritpion, thne detoggle the \"Privatize\" setting under publicity.\n\nHave fun making something awsome, and I deeply thank you for contributing to lauch pad's community </pre>`
# });

def publicize(project_id, settings):
    print("publicizing")
    project = supabase.table("projects").select("project_page").eq("project_id", project_id).execute().data[0]
    page = project.get("project_page")
    page["_value"]["public"] = True
    supabase.table("projects").update({"project_page": page, "is_public": True}).eq("project_id", project_id).execute()

    mainCard = supabase.table("projects").select("project_page").eq("project_id", project_id).execute().data[0].get("project_page").get("_value").get("mainCard")
    member_count = len(supabase.table("projects").select("members_info").eq("project_id", project_id).execute().data[0].get("members_info"))

    try: 
        if len(supabase.table("search_table").select("*").eq("project_id", project_id).execute().data) > 0:
            
            supabase.table("search_table").update({
                                            "type": "project",
                                            "project_id": project_id, 
                                            "title": mainCard.get("title"),
                                            "description": settings.get("description"),
                                            "image_url": mainCard.get("image"),
                                            "lat": mainCard.get("coordinates").get("lat"),
                                            "lng": mainCard.get("coordinates").get("lng"),
                                            "location": mainCard.get("location"),
                                            "time_posted": serialize_datetime(datetime.now()),
                                            "member_count": member_count,
                                            "remote": settings.get("remote_friendly"),
                                            "physical": not settings.get("remove_physical_locations")
                                        }).eq("project_id", project_id).execute()
            
            # roles = supabase.table("projects").select("roles").eq("project_id", project_id).execute().data[0].get("roles")
            # for role in roles:
            #     job = supabase.table("jobs").select("*").eq("job_id", role).execute().data[0]
            #     if(not job.get("closed")):
            #         if len(supabase.table("search_table").select("*").eq("project_id", project_id).eq("job_id", role).execute().data) > 0:
            #             supabase.table("search_table").update({
            #                 "type": "job",
            #                 "lat": mainCard.get("coordinates").get("lat"),
            #                 "lng": mainCard.get("coordinates").get("lng"),
            #                 "physical": not settings.get("remove_physical_locations"),
            #                 "remote": settings.get("remote_friendly"),
            #                 "location": mainCard.get("location"),
            #                 "title": job.get("job_object").get("jobDescription").get("title")[0],
            #                 "description": job.get("job_object").get("jobDescription").get("summary")[0],
            #                 "time_posted": serialize_datetime(datetime.now())
            #             }).eq("project_id", project_id).eq("job_id", role).execute()
            #         else:
            #             supabase.table("search_table").insert({
            #                 "job_id": role,
            #                 "project_id": project_id,
            #                 "type": "job",
            #                 "lat": mainCard.get("coordinates").get("lat"),
            #                 "lng": mainCard.get("coordinates").get("lng"),
            #                 "physical": not settings.get("remove_physical_locations"),
            #                 "remote": settings.get("remote_friendly"),
            #                 "location": mainCard.get("location"),
            #                 "title": job.get("job_object").get("jobDescription").get("title")[0],
            #                 "description": job.get("job_object").get("jobDescription").get("summary")[0],
            #                 "time_posted": serialize_datetime(datetime.now())
            #             }).execute()
        else:
            supabase.table("search_table").insert({
                                "type": "project",
                                "project_id": project_id, 
                                "title": mainCard.get("title"),
                                "description": settings.get("description"),
                                "image_url": mainCard.get("image"),
                                "lat": mainCard.get("coordinates").get("lat"),
                                "lng": mainCard.get("coordinates").get("lng"),
                                "location": mainCard.get("location"),
                                "time_posted": serialize_datetime(datetime.now()),
                                "member_count": member_count,
                                "remote": settings.get("remote_friendly"),
                                "physical": not settings.get("remove_physical_locations")
                            }).execute()
            roles = supabase.table("projects").select("roles").eq("project_id", project_id).execute().data[0].get("roles")
            for role in roles:
                job = supabase.table("jobs").select("*").eq("job_id", role).execute().data[0]
                
                if(not job.get("closed")):
                    supabase.table("search_table").insert({
                        "job_id": role,
                        "project_id": project_id,
                        "type": "job",
                        "lat": mainCard.get("coordinates").get("lat"),
                        "lng": mainCard.get("coordinates").get("lng"),
                        "physical": not settings.get("remove_physical_locations"),
                        "remote": settings.get("remote_friendly"),
                        "location": mainCard.get("location"),
                        "title": job.get("job_object").get("jobDescription").get("title")[0],
                        "description": job.get("job_object").get("jobDescription").get("summary")[0],
                        "time_posted": serialize_datetime(datetime.now())
                    }).execute()


    except Exception as e:
        print("Error inserting into search table:", str(e))

def close_project(project_id):
    supabase.table("search_table").delete().eq("project_id", project_id).execute()
    supabase.table("projects").update({"is_public": False}).eq("project_id", project_id).execute()

class process_request:
    def post(request, project_id):
        try:
            data = json.loads(request.body)
            supabase.from_("projects").update({"settings": data.get("settings")}).eq("project_id", project_id).execute()
            page = supabase.table("projects").select("project_page").eq("project_id", project_id).execute().data[0].get("project_page")
            page["_value"]["mainCard"]["remote"] = data.get("settings").get("remote_friendly")
            page["_value"]["mainCard"]["physicalLocation"] = data.get("settings").get("remove_physical_locations")
            supabase.from_("projects").update({"project_page": page}).eq("project_id", project_id).execute()

            if not data.get("settings").get("private_project"):
                publicize(project_id, data.get("settings"))
            else:
                close_project(project_id)

            return JsonResponse({"message": "Project settings updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
