from django.urls import include, path

from . import views

urlpatterns = [
    path("/<user_id>/<friend_id>", views.testView.as_view(), name="is_friends"),
]