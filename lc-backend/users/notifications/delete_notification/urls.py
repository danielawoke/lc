from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>/<str:notification_id>", views.DeleteNotificationView.as_view(), name="delete_notifications"),
]