from django.urls import path, include
from . import views

urlpatterns = [
    path("/<str:project_id>/<str:view_mode>", views.testView.as_view(), name="index"),
]