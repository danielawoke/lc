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

def gen_unique_proposal_id():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("proposal_data").select("proposal_id").eq("proposal_id", new_id).execute()
        if len(response.data) == 0:
            return new_id 


class proposal_assessment:

    def detect_delegate_cycle(user_id, proposal_id, delegate_id):
        visited = set()
        current_id = delegate_id

        while current_id is not None:
            if current_id == user_id:
                return True  # Cycle detected
            if current_id in visited:
                return True
            visited.add(current_id)

            # Fetch the next delegate in the chain
            next_delegate = supabase.table("proposals").select("delegate_id").eq("user_id", current_id).eq("proposal_id", proposal_id).execute().data
            if len(next_delegate) == 0:
                break  # No further delegation
            current_id = next_delegate[0].get("delegate_id")
        return False 

    def get_delegate_vote(proposal_id, delegate_id):
        delegate_vote = supabase.table("proposals").select("vote").eq("user_id", delegate_id).eq("proposal_id", proposal_id).execute().data
        if len(delegate_vote) == 0:
            return None
        return delegate_vote[0].get("vote")

    def assess_proposal(proposal):
        proposal_data = supabase.table("proposals").select("*").eq("proposal_id", proposal).execute().data
        if len(proposal_data) == 0:
            return

        vote_count = len(proposal_data)
        in_favor = 0
        against = 0
        abstain = 0
        for vote in proposal_data:
            print(vote)
            if vote.get("vote") == "in favor":
                in_favor += 1
            elif vote.get("vote") == "against":
                against += 1
            elif vote.get("vote") == "withdraw":
                abstain += 1
            elif vote.get("vote") == "delegate":
                delegate_vote = proposal_assessment.get_delegate_vote(proposal, vote.get("delegate_id"))
                print(delegate_vote)
                if delegate_vote == "in favor":
                    in_favor += 1
                elif delegate_vote == "against":
                    against += 1
                elif delegate_vote == "withdraw":
                    # add reauthorize settings here in the vote itself
                    abstain += 1

        total = vote_count - abstain
        
        if(total == 0):
            clearProposal(proposal)
        if float(in_favor/total) > 0.5:
            type = proposal_data[0].get("proposal_meta_cache").get("type")
            if type == "Start Discussion":
                startDiscussion(proposal)
            elif type == "Offer Position":
                offerPosition(proposal)
            elif type == "Remove Member":
                remove_memeber(proposal)
            elif type == "Direct Invite":
                directInvite(proposal)
            clearProposal(proposal)
        elif float(against/total) > 0.5:
            print("fail")
            clearProposal(proposal)
        else:
            print("no majority")



def clearProposal(proposal_id):
    supabase.table("proposals").delete().eq("proposal_id", proposal_id).execute()
    supabase.table("proposal_data").delete().eq("proposal_id", proposal_id).execute()
    

def directInvite(proposal):
    try:

        usertag = supabase.table("proposal_data").select("proposal_body").eq("proposal_id", proposal).execute().data[0].get("proposal_body").get('usertag')
        userid = supabase.table("users").select("user_id").eq("user_tag", usertag).execute().data[0].get("user_id")
        project_id = supabase.table("proposals").select("project_id").eq("proposal_id", proposal).execute().data[0].get("project_id")
        project_name = supabase.table("projects").select("*").eq("project_id",project_id).execute().data[0].get("project_page").get("_value").get("mainCard").get("title")

        try:
            supabase.table("notifications").insert({
                "title":"Project Invite", 
                "text_summary": f"""Youve been invited to join {project_name}""",
                "HTML":f"""
                        <div style='color:white; font-family: Arial, Helvetica, sans-serif; font-size: 14px; width:fit-content; border-radius: 10px;'>
                            <div>You've been invited to join <b>{project_name}</b>. Click the button bellow to accept.</div>
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
        except Exception as error:
            print(str(error))

    except Exception as e:
        print(str(e))

def remove_memeber(proposal):
    try:
        usertag = supabase.table("proposal_data").select("proposal_body").eq("proposal_id", proposal).execute().data[0].get("proposal_body").get('usertag')
        user_id = supabase.table("users").select("user_id").eq("user_tag", usertag).execute().data[0].get("user_id")
        
        project_id = supabase.table("proposals").select("project_id").eq("proposal_id", proposal).execute().data[0].get("project_id")

        members = supabase.table("projects").select("members_info").eq("project_id", project_id).execute().data[0].get("members_info")
        members = [member for member in members if member.get("user_id") != user_id]
        supabase.table("projects").update({"members_info": members}).eq("project_id", project_id).execute()

        config_settings = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data[0].get("members_config")
        config_settings = [config for config in config_settings if config.get("member_id") != user_id]
        supabase.table("projects").update({"members_config": config_settings}).eq("project_id", project_id).execute()

        supabase.table("proposals").delete().eq('user_id', user_id ).eq("project_id", project_id).execute()
        supabase.table("new_candidates").delete().eq('user_id', user_id ).eq("project_id", project_id).execute()

        count = supabase.table("users").select("project_count").eq("user_id", user_id).execute().data[0].get("project_count")
        supabase.table("users").update({"project_count", count - 1}).eq("user_id", user_id).execute()

    except Exception as e:
        print(str(e))
    return

def create_unique_chatroom_UUID():
    while True:
        new_id = str(uuid.uuid4())
        response = supabase.table("messages").select("chat_room_id").eq("chat_room_id", new_id).execute()
        if len(response.data) == 0:
            return new_id

def offerPosition(proposal):
    try:
        project_id = supabase.table("proposals").select("project_id").eq("proposal_id", proposal).execute().data[0].get("project_id")
        application_id = supabase.table("proposal_data").select("application_id").eq("proposal_id", proposal).execute().data[0].get("application_id")
        job_id = supabase.table("applicants").select("job_id").eq("application_id", application_id).execute().data[0].get("job_id")
        application_data = supabase.table("applicants").select("application_object").eq("application_id", application_id).execute().data[0].get("application_object")
        usertag = application_data.get("usertag")
        userid = supabase.table("users").select("user_id").eq("user_tag", usertag).execute().data[0].get("user_id")

        project_name = supabase.table("projects").select("*").eq("project_id",project_id).execute().data[0].get("project_page").get("_value").get("mainCard").get("title")
        job_name = supabase.table("jobs").select("*").eq("job_id",job_id).execute().data[0].get("job_object").get("jobDescription").get("title")[0]

        supabase.table("notifications").insert({
            "title":"Position Offered", 
            "text_summary": f"""Congrats!, you've been offered the {job_name} position at {project_name}""",
            "HTML":f"""
                    <div style='color:white; font-family: Arial, Helvetica, sans-serif; font-size: 14px; width:fit-content; border-radius: 10px;'>
                        <div>Congrats! You've been offered the <b>{job_name}</b> position at <b>{project_name}</b>. Click the button bellow to accept.</div>
                        <button style="margin-top:20px; padding:10px; background-color: rgb(0, 183, 255); border:none; border-radius:5px; color:white; cursor:pointer; display:block;"
                                id="accept-offer-button" proposal_id="{proposal}">
                            Accept Offer
                        </button>
                    </div>
                """,
            "time": serialize_datetime(datetime.now()),
            "user_id": userid,
            "read":False
        }).execute()
    except Exception as e:
        print(str(e))
    return

def startDiscussion(proposal):
    project_id = supabase.table("proposals").select("project_id").eq("proposal_id", proposal).execute().data[0].get("project_id")
    chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")
    application_id = supabase.table("proposal_data").select("application_id").eq("proposal_id", proposal).execute().data[0].get("application_id")
    application_data = supabase.table("applicants").select("application_object").eq("application_id", application_id).execute().data[0].get("application_object")
    job_id = supabase.table("applicants").select("job_id").eq("application_id", application_id).execute().data[0].get("job_id")
    room_id = create_unique_chatroom_UUID()
    supabase.table("messages").insert({"chat_room_id": room_id, "user_id": "-1"}).execute()

    infavorData = supabase.table("proposals").select("*").eq("proposal_id", proposal).eq("vote", "in favor").execute().data
    infavor = []
    for proposal in infavorData:
        infavor.append({"name": proposal.get("profile_data_cache").get("name"), "image": proposal.get("profile_data_cache").get("profile_image")})

    againstData = supabase.table("proposals").select("*").eq("proposal_id", proposal).eq("vote", "against").execute().data
    against = []
    for proposal in againstData:
        against.append({"name": proposal.get("profile_data_cache").get("name"), "image": proposal.get("profile_data_cache").get("profile_image")})

    applicant_id = supabase.table("users").select("user_id").eq("user_tag", application_data.get("usertag")).execute().data[0].get("user_id")

    try:
        for job in chat_layout.get("Discussions"):

            if job.get("job_id") == job_id:
                discussion = {
                    "chat_id": room_id,
                    "name": application_data.get("name"),
                    "user_id": applicant_id,
                    "usertag": application_data.get("usertag"),
                    "application_id": application_id,
                    "proposal_saved": {
                        "note": supabase.table("proposal_data").select("note").eq("proposal_id", proposal.get("proposal_id")).execute().data[0].get("note"),
                        "against": against,
                        "in favor": infavor,
                        "application_object": application_data
                    }
                }
                job.get("Candidates").append(discussion)
                supabase.table("projects").update({"chat_layout": chat_layout}).eq("project_id", project_id).execute()
                break

        mainCard = supabase.table("projects").select("project_page").eq("project_id", project_id).execute().data[0].get("project_page").get("_value").get("mainCard")
        job_name = supabase.table("jobs").select("*").eq("job_id", job_id).execute().data[0].get("job_object").get("jobDescription").get("title")[0]
        roomTitle = job_name + " @ " + mainCard.get("title")
        supabase.table("chat_room_relations").insert({"chat_room_id": room_id, "user_id": applicant_id, "relation": "interviews", "room_name": roomTitle, "room_image": mainCard.get("image")}).execute()
        supabase.table("last_message_times").insert({"chat_room_id": room_id, "last_update_time": serialize_datetime(datetime.now()), "project_id": project_id, "job_id": job_id}).execute()
    
    except Exception as e:
        print(str(e))



class process_request:
    def post(request, project_id, user_id, job_id):
        proposal_id = gen_unique_proposal_id()
        try:
            # add anonymity of user later
            request_data = json.loads(request.body)
            type = request_data.get("type")
            if type == "Start Discussion":

                profile_data = supabase.table("users").select("*").eq("user_id", user_id).execute().data
                profile_data_cache = {
                    "name": profile_data[0].get("profile_data").get("display_name"),
                    "profile_image": profile_data[0].get("profile_data").get("UserImage"),
                    "user_tag": profile_data[0].get("user_tag")
                }
                
                application_data = request_data.get("application_data")
                proposal_meta_cache = {
                    "name":application_data.get("name"),
                    "role": application_data.get("job"),
                    "type": type
                }
                note = request_data.get("context")
                supabase.table("proposal_data").insert({"proposal_id": proposal_id, "proposal_body": application_data, "note": note, "application_id": request_data.get("application_id"), "project_id": project_id}).execute()
                project_memeber_list = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data
                project_memeber_list = project_memeber_list[0].get("members_config")

                for member_config_settings in project_memeber_list:

                    currentUserProfile = supabase.table("users").select("*").eq("user_id", member_config_settings.get("member_id")).execute().data

                    currentUserProfileCache = {
                        "name": currentUserProfile[0].get("profile_data").get("display_name"),
                        "profile_image": currentUserProfile[0].get("profile_data").get("UserImage"),
                        "user_tag": currentUserProfile[0].get("user_tag")
                    }

                    if member_config_settings.get("member_id") == user_id:
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "in favor", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache}).execute()
                        continue

                    if member_config_settings.get("configSettings").get("withdraw_from_all"):
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                        continue

                    delegated_jobs = member_config_settings.get("configSettings").get("delegated_jobs")
                    for job in delegated_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "delegate", "delegate_id": job.get("delegate_id"), "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache}).execute()
                            continue 
                    
                    withdraw_jobs = member_config_settings.get("configSettings").get("withdrawn_jobs")
                    
                    for job in withdraw_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                            continue 

                    supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": False, "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()

                application_id = request_data.get("application_id")
                supabase.table("new_candidates").delete().eq("application_id", application_id).eq("user_id", user_id).execute()
            elif type == "Offer Position":

                profile_data = supabase.table("users").select("*").eq("user_id", user_id).execute().data
                
                profile_data_cache = {
                    "name": profile_data[0].get("profile_data").get("display_name"),
                    "profile_image": profile_data[0].get("profile_data").get("UserImage"),
                    "user_tag": profile_data[0].get("user_tag")
                }

                chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")

                application_id = None
                try:
                    application_job_id = request_data.get("offer_position_data").get("job_id")
                    user_tag = request_data.get("offer_position_data").get("proposal").get("application_object").get("usertag")
                    
                    for job in chat_layout.get("Discussions"):
                        if job.get("job_id") == application_job_id:
                            for candidate in job.get("Candidates"):
                                if candidate.get("usertag") == user_tag:
                                    application_id = candidate.get("application_id")
                                    break

                    chat_layout = supabase.table("projects").select("chat_layout").eq("project_id", project_id).execute().data[0].get("chat_layout")
                    chat_layout.append(proposal_id)
                except Exception as e:
                    print(str(e))

                print(application_id)

                note = request_data.get("context")

                proposal_meta_cache = {
                    "name":request_data["offer_position_data"].get("proposal").get("application_object").get("name"),
                    "role": request_data["offer_position_data"].get("proposal").get("application_object").get('role'),
                    "type": type
                }
                
                application_data = {
                    "job": request_data["offer_position_data"].get("proposal").get("application_object").get("role"),
                    "name": request_data["offer_position_data"].get("proposal").get("application_object").get("name"),
                    # Need to replace
                    "usertag": None,
                    "questions": request_data["offer_position_data"].get("proposal").get("application_object").get("questions")
                }

                supabase.table("proposal_data").insert({"proposal_id": proposal_id, "proposal_body": application_data, "note": note, "application_id": application_id}).execute()
                project_memeber_list = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data
                project_memeber_list = project_memeber_list[0].get("members_config")

                for member_config_settings in project_memeber_list:

                    currentUserProfile = supabase.table("users").select("*").eq("user_id", member_config_settings.get("member_id")).execute().data
                    
                    currentUserProfileCache = {
                        "name": currentUserProfile[0].get("profile_data").get("display_name"),
                        "profile_image": currentUserProfile[0].get("profile_data").get("UserImage"),
                        "user_tag": currentUserProfile[0].get("user_tag")
                    }


                    if member_config_settings.get("member_id") == user_id:
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": user_id, "proposal_id": proposal_id, "voted": True, "vote": "in favor", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache   }).execute()
                        continue

                    if member_config_settings.get("configSettings").get("withdraw_from_all"):
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                        continue

                    delegated_jobs = member_config_settings.get("configSettings").get("delegated_jobs")
                    for job in delegated_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "delegate", "delegate_id": job.get("delegate_id"), "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache}).execute()
                            continue 
                    
                    withdraw_jobs = member_config_settings.get("configSettings").get("withdrawn_jobs")
                    
                    for job in withdraw_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                            continue 

                    supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": False, "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
            elif type == "Remove Member":
                
                note = request_data.get("context")
                name = request_data["remove_member_data"].get("name")

                profile_data = supabase.table("users").select("*").eq("user_id", user_id).execute().data

                profile_data_cache = {
                    "name": profile_data[0].get("profile_data").get("display_name"),
                    "profile_image": profile_data[0].get("profile_data").get("UserImage"),
                    "user_tag": profile_data[0].get("user_tag")
                }

                proposal_meta_cache = {
                    "name":name,
                    "type": type
                }
                
                application_data = {
                    "name": name,
                    "usertag": request_data["remove_member_data"].get("usertag"),
                }


                supabase.table("proposal_data").insert({"proposal_id": proposal_id, "proposal_body": application_data, "note": note}).execute()
                project_memeber_list = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data
                project_memeber_list = project_memeber_list[0].get("members_config")

                for member_config_settings in project_memeber_list:

                    currentUserProfile = supabase.table("users").select("*").eq("user_id", member_config_settings.get("member_id")).execute().data
                    
                    currentUserProfileCache = {
                        "name": currentUserProfile[0].get("profile_data").get("display_name"),
                        "profile_image": currentUserProfile[0].get("profile_data").get("UserImage"),
                        "user_tag": currentUserProfile[0].get("user_tag")
                    }

                    if member_config_settings.get("member_id") == user_id:
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": user_id, "proposal_id": proposal_id, "voted": True, "vote": "in favor", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache   }).execute()
                        continue

                    if member_config_settings.get("configSettings").get("withdraw_from_all"):
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                        continue

                    delegated_jobs = member_config_settings.get("configSettings").get("delegated_jobs")
                    for job in delegated_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "delegate", "delegate_id": job.get("delegate_id"), "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache}).execute()
                            continue 
                    
                    withdraw_jobs = member_config_settings.get("configSettings").get("withdrawn_jobs")
                    
                    for job in withdraw_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                            continue 

                    supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": False, "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
            elif type == "Direct Invite":
                
                note = request_data.get("context")
                tag = request_data.get("inviteTag")

                display_name_response = supabase.table("users").select("profile_data").eq("user_tag", tag).execute().data
                display_name_response = display_name_response[0].get("profile_data").get("display_name")
                name = display_name_response

                profile_data = supabase.table("users").select("*").eq("user_id", user_id).execute().data

                profile_data_cache = {
                    "name": profile_data[0].get("profile_data").get("display_name"),
                    "profile_image": profile_data[0].get("profile_data").get("UserImage"),
                    "user_tag": profile_data[0].get("user_tag")
                }

                proposal_meta_cache = {
                    "name":name,
                    "type": type
                }
                
                application_data = {
                    "name": name,
                    "usertag": tag,
                }

                supabase.table("proposal_data").insert({"proposal_id": proposal_id, "proposal_body": application_data, "note": note}).execute()
                project_memeber_list = supabase.table("projects").select("members_config").eq("project_id", project_id).execute().data
                project_memeber_list = project_memeber_list[0].get("members_config")

                for member_config_settings in project_memeber_list:
                    
                    currentUserProfile = supabase.table("users").select("*").eq("user_id", member_config_settings.get("member_id")).execute().data
                    
                    currentUserProfileCache = {
                        "name": currentUserProfile[0].get("profile_data").get("display_name"),
                        "profile_image": currentUserProfile[0].get("profile_data").get("UserImage"),
                        "user_tag": currentUserProfile[0].get("user_tag")
                    }

                    if member_config_settings.get("member_id") == user_id:
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": user_id, "proposal_id": proposal_id, "voted": True, "vote": "in favor", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache   }).execute()
                        continue

                    if member_config_settings.get("configSettings").get("withdraw_from_all"):
                        supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                        continue

                    delegated_jobs = member_config_settings.get("configSettings").get("delegated_jobs")
                    for job in delegated_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "delegate", "delegate_id": job.get("delegate_id"), "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache}).execute()
                            continue 
                    
                    withdraw_jobs = member_config_settings.get("configSettings").get("withdrawn_jobs")
                    
                    for job in withdraw_jobs:
                        if job.get("job_id") == job_id:
                            supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": True, "vote": "withdraw", "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()
                            continue 

                    supabase.table("proposals").insert({"project_id": project_id, "user_id": member_config_settings.get("member_id"), "proposal_id": proposal_id, "voted": False, "profile_data_cache": currentUserProfileCache, "proposal_meta_cache": proposal_meta_cache }).execute()

            proposal_assessment.assess_proposal(proposal_id)
            return JsonResponse({"message": "Proposal created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)