from django.urls import include, path

from . import views

urlpatterns = [
    path("load", include("messages.load.urls")),
    path("send", include("messages.send.urls")),
    path("auto_load", include("messages.auto_load.urls")),
    path("create_room", include("messages.create_room.urls")),
]