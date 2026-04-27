from django.urls import path, include
from . import views

urlpatterns = [
    path("/<str:project_id>", views.testView.as_view(), name="index"),
]