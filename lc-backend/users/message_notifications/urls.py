from django.urls import include, path

from . import views

urlpatterns = [
    path("/load", include("users.message_notifications.load.urls")),
    path("/in_chat_room", include("users.message_notifications.in_chat_room.urls")),
    path("/enable_notifications", include("users.message_notifications.enable_notifications.urls")),
    path("/is_notifications_enabled", include("users.message_notifications.is_notifications_enabled.urls")),
    path("/enable_project_notifications", include("users.message_notifications.enable_project_notifications.urls")),
]