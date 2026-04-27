from django.urls import include, path

from . import views

urlpatterns = [
    path("/load_rooms", include("projects.discussions.load_rooms.urls")),
    path("/create_general_room", include("projects.discussions.create_genearl_room.urls")),
    path("/delete_room", include("projects.discussions.delete_room.urls")),
    path("/edit_room_name", include("projects.discussions.edit_room_name.urls")),
]