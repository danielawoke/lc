from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>/<str:chat_room_id>", views.view.as_view()),
]