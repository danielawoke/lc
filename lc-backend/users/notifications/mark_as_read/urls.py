from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>/<str:notification_id>", views.MarkAsReadView.as_view(), name="mark_as_read"),
]