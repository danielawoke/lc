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


def create_unique_project_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("projects").select("project_id").eq("project_id", new_id).execute()
        if len(response.data) == 0:
            return new_id

def create_unique_job_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("jobs").select("job_id").eq("job_id", new_id).execute()
        if len(response.data) == 0:
            return new_id
        
def create_unique_chat_room_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("chat_room_relations").select("chat_room_id").eq("chat_room_id", new_id).execute()
        if len(response.data) == 0:
            return new_id

def send_invite(invite, project_id, project_meta):
    print(invite)
    userid = supabase.table("users").select("user_id").eq("user_tag", invite).execute().data[0].get("user_id")
    supabase.table("notifications").insert({
                "title":"Project Invite", 
                "text_summary": f"""Youve been invited to join {project_meta.get('title')}""",
                "HTML":f"""
                        <div style='color:white; font-family: Arial, Helvetica, sans-serif; font-size: 14px; width:fit-content; border-radius: 10px;'>
                            <div>You've been invited to join <b>{project_meta.get('title')}</b>. Click the button bellow to accept.</div>
                            <button style="margin-top:20px; padding:10px; background-color: rgb(0, 183, 255); border:none; border-radius:5px; color:white; cursor:pointer; display:block;"
                                    id="accept-offer-button" project_id="{project_id}">
                                Accept Offer
                            </button>
                        </div>
                    """,
                "time": serialize_datetime(datetime.now()),
                "user_id": userid,
                "read":False
            }).execute()

class process_request:
    def post(request):
        

        project_id = create_unique_project_UUID()
        response = json.loads(request.body)
        project_meta = response.get("project_meta")
        project_page = response.get("project_page")
        members = [response.get("creator_id")]
        chat_room_id = create_unique_chat_room_UUID()
        job_uuid = create_unique_job_UUID()
        jobs = [job_uuid]
        invites = response.get("invites")

        # creator_profile = supabase.table("users").select("*").eq("user_id",response.get("creator_id")).execute().data[0]
        # prem = creator_profile.get("Premium")
        # proj_count = creator_profile.get("project_count")
        
        # if proj_count >= 10000 and prem == "free":
        #     return JsonResponse({"message": "Memebership required to be a part of more projects"}, status=400)

        Any_default_job =  {
                "jobDescription": {
                    "title": ["Any"],
                    "description": ["""Anyone can apply to this role, and we will work with you to find the best fit for you in our project!<div data-v-077883e2="" id="editor"></div>"""],  
                    "summary": ["Anyone of any background, show us your skills, and we'll see if we can make a place for you!"]
                },
                "jobQuestions": {
                    "resume":["optional"],
                    "contacts": [["Email",1,"base"], ["Phone",0,"base"], ["IP-address",0,"base"]],
                    "anonymous": [False],
                    "extraQuestion": [
                        {
                            "type":"free-form",
                            "questionHTML": ["What you can do to help us?"],
                            "questionType": ["freeform"],
                            "maxWord": [None, False],
                            "minWord": [None, False],
                            "isOptional": [True]
                        },
                    ]
                },
                "color": {
                    "backgroundColor": ["white"],
                    "textColor": ["black"]
                },
                "settings": {
                    "closed": [False],
                    "maxApplications": [False, 100 ],
                    "applicationDeadline": [False, None ],
                }
            }
            
        default_settings =  {
                                "private_project": True,
                                "remote": False,
                                "remove_physical_locations": response.get("project_meta").get("physicalLocation"),
                                "description": "",
                                "remote_friendly": response.get("project_meta").get("remoteFriendly"),
                            }

        chat_layout = {
                        "Genearl": [
                            {
                                "name": "Main",
                                "chat_id": chat_room_id
                            }
                        ],
                        "Discussions": [
                            {
                                "Job": "Any",
                                "job_id": job_uuid,
                                "Candidates": []
                            }
                        ]
                    }
        
        supabase.table("messages").insert({"chat_room_id": chat_room_id, "user_id": "-1"}).execute()

        config_settings = [
                        {
                            "member_id": response.get("creator_id"),
                            "configSettings": {
                                "delegated_jobs": [],
                                "withdrawn_jobs": [],
                                "withdraw_from_all": False,
                                "reject_remaining_enabled": False
                            }
                        }
                    ]
        
        creator_info = supabase.table("users").select("*").eq("user_id", response.get("creator_id")).execute().data[0]
        
        members_info = [
                        {
                            "name": creator_info.get("profile_data").get("display_name"),
                            "image": creator_info.get("profile_data").get("UserImage"),
                            "user_id": response.get("creator_id"),
                            "usertag": creator_info.get("user_tag")
                        },
                    ]
        
        try:
            supabase.table("jobs").insert({"job_id": job_uuid, "project_id": project_id, "job_object": Any_default_job}).execute()
            supabase.table("projects").insert({"project_id": project_id, 
                                               "project_meta": project_meta, 
                                               "project_page": project_page, 
                                               "members": members, 
                                               "roles": jobs, 
                                               "settings": default_settings,
                                               "chat_layout": chat_layout,
                                               "members_config": config_settings,
                                               "members_info": members_info,
                                               "is_public": False
                                            }).execute()
            for invite in invites:
                send_invite(invite, project_id, project_meta)

            return JsonResponse({"message": "Project created successfully", "project_id": project_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    