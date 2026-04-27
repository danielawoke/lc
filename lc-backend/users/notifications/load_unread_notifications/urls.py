from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>", views.LoadUnreadNotificationsView.as_view(), name="load_unread_notifications"),
]