from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.view.as_view()),
    path("/set-tag", include("users.create.set_tag.urls")),
    path("/complete-profile", include("users.create.complete_profile.urls")),
]