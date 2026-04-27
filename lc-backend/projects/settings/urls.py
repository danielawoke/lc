from django.urls import include, path

from . import views

urlpatterns = [
    path("/edit", include("projects.settings.edit.urls")),
    path("/load", include("projects.settings.load.urls")),
]