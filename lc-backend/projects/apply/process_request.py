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
        response = supabase.table("applicants").select("application_id").eq("application_id", new_id).execute()
        if len(response.data) == 0:
            return new_id

class process_request:
    def post(request):
        
        request_data = json.loads(request.body)

        applicant_profile = supabase.table("users").select("*").eq("user_id", request_data.get("userID")).execute().data[0]

        tag = applicant_profile.get("user_tag")
        name = applicant_profile.get("profile_data").get("display_name")
        job_title = request_data.get("jobInfo").get("jobDescription").get("title")[0]

        contacts = request_data.get("contactInfo")
        resume = request_data.get("resume")
        extra =  request_data.get("jobInfo").get("jobQuestions").get("extraQuestion")
        responses = []

        for contact in contacts:
            contactType = contact[0]
            val = contact[1]
            responses.append({"question": contactType, "response": val})

        if resume != None:
            responses.append({"question": "resume", "response": resume})

        for i in range(len(extra)):
            question = extra[i]
            responses.append({"question": question.get("questionHTML")[0], "response": request_data.get("responses")[i].get("response")})
            
        application_object = {
            "name": name,
            "project_id": request_data.get("projectID"),
            "usertag": tag,
            "job": job_title,
            "questions": responses,
        }

        applicant_id = create_unique_job_UUID()

        supabase.table("applicants").insert({
                                             "application_id": applicant_id, 
                                             "rejection_information": [],
                                             "user_id": request_data.get("userID"),
                                             "application_object": application_object,
                                             "job_id": request_data.get("jobID"),
                                             "project_name": request_data.get("projectName"),
                                             "date_created": serialize_datetime(datetime.now()),
                                             "status": "Pending"
                                            }).execute()
        
        preview_data = {
                        "job": job_title,
                        "name": name,
                        "application_id": applicant_id,
                        "description": request_data.get("selfStatement"),
                        "image": applicant_profile.get("profile_data").get("UserImage"),
                    }
        
        project_config = supabase.table("projects").select("*").eq("project_id", request_data.get("projectID")).execute().data[0].get("members_config")
        for member in project_config:

            if member.get("configSettings").get("withdraw_from_all"):
                continue
            if member.get("configSettings").get("delegated_jobs") and any(job.get("job_id") == request_data.get("jobID") for job in member.get("configSettings").get("delegated_jobs")):
                continue
            if member.get("configSettings").get("withdrawn_jobs") and any(job.get("job_id") == request_data.get("jobID") for job in member.get("configSettings").get("withdrawn_jobs")):
                continue
            supabase.table("new_candidates").insert({"user_id": member.get("member_id"), "project_id": request_data.get("projectID"), "application_id": applicant_id, "job_id": request_data.get("jobID"), "preview_data": preview_data}).execute()

        return JsonResponse({"message": "Application submitted successfully"}, status=201)
    
 