from django.urls import include, path

from . import views

urlpatterns = [
    path("/delete_notification", include("users.notifications.delete_notification.urls"), name="delete_notifications"),
    path("/load_notifications", include("users.notifications.load_notifications.urls"), name="load_notifications"),
    path("/load_unread_notifications", include("users.notifications.load_unread_notifications.urls"), name="load_unread_notifications"),
    path("/mark_as_read", include("users.notifications.mark_as_read.urls"), name="mark_as_read"),
]