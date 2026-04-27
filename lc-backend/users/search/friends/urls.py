from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:usertag>", views.testView.as_view(), name="friends"),
]