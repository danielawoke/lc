from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:project_id>/<str:user_id>/<str:job_id>/", views.load_applicant_info.as_view(), name="load_applicant_info"),
]