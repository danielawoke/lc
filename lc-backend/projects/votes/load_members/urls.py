from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:project_id>", views.load_members.as_view(), name="load_members"),
]