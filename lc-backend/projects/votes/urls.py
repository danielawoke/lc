from django.urls import include, path

from . import views

urlpatterns = [
    path("/load_candidates", include("projects.votes.load_candidates.urls"), name="load_candidates"),
    path("/load_applicant_info", include("projects.votes.load_applicant_data.urls"), name="load_applicant_info"),
    path("/load_proposals", include("projects.votes.load_proposals.urls"), name="load_proposals"),
    path("/load_proposal_data", include("projects.votes.load_proposal_data.urls"), name="proposal_data"),
    path("/cast_vote", include("projects.votes.cast_vote.urls"), name="cast_vote"),
    path("/current_voters", include("projects.votes.current_voters.urls"), name="current_voters"),
    path("/create_proposal", include("projects.votes.create_proposal.urls"), name="create_proposal"),
    path("/load_config_settings", include("projects.votes.load_config_settings.urls"), name="load_config_settings"),
    path("/update_config", include("projects.votes.update_config.urls"), name="update_config"),
    path("/load_discussions", include("projects.votes.load_discussions.urls"), name="load_discussions"),
    path("/load_members", include("projects.votes.load_members.urls"), name="load_members"),
    path("/load_signed_proposals", include("projects.votes.load_signed_proposals.urls"), name="load_signed_proposals"),
    path("/reject", include("projects.votes.reject.urls"), name="reject"),
    path("/load_reject", include("projects.votes.load_reject.urls"), name="load_reject"),
]