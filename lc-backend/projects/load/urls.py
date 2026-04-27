from django.urls import include, path

from . import views

urlpatterns = [
    path("/admin", include("projects.load.admin.urls")),
    path("/public", include("projects.load.public.urls")),
    
]