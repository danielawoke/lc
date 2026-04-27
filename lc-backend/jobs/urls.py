from django.urls import include, path

from . import views

urlpatterns = [
    path("project-load", include("jobs.project_load.urls")),
    path("new_job", include("jobs.new_job.urls")),
    path("update_job", include("jobs.update_job.urls")),
    path("delete_job", include("jobs.delete_job.urls")),
]

# These end points need to be secured so only members can use them, right not thats not the case