from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:project_id>", views.testView.as_view(), name="index"),
]