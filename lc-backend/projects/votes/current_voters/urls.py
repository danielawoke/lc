from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:proposal_id>", views.load_applicant_info.as_view(), name="load_applicant_info"),
]