from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>", views.LoadNotificationsView.as_view(), name="load_notifications"),
]