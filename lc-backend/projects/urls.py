from django.urls import include, path

from . import views

urlpatterns = [
    path("create", include("projects.create.urls")),
    path("admin-load", include("projects.admin_load.urls")),
    path("update-page", include("projects.update_page.urls")),
    path("votes", include("projects.votes.urls")),
    path("apply", include("projects.apply.urls")),
    path("discussions", include("projects.discussions.urls")),
    path("settings", include("projects.settings.urls")),
    path("leave", include("projects.leave.urls")),
    path("load", include("projects.load.urls")),
]