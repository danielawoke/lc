from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:chat_room_id>/<str:last_message_time>", views.testView.as_view()),
]