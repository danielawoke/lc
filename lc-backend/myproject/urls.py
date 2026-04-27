from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("refrence.urls")),
    path("users/", include("users.urls")),
    path("search/", include("search.urls")),
    path("admin/", admin.site.urls),
    path("messages/", include("messages.urls")),
    path("projects/", include("projects.urls")),
    path("jobs/", include("jobs.urls")),
]