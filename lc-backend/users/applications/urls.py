from django.urls import include, path

from . import views

urlpatterns = [
    path("/load", include("users.applications.load.urls")),
    path("/delete", include("users.applications.delete.urls"))
]