from django.urls import include, path

from . import views

urlpatterns = [
    path("/account_setup", include("users.search.account_setup.urls")),
    path("/full_profile", include("users.search.full_profile.urls")),
    path("/search_by_usertag", include("users.search.search_by_usertag.urls")),
    path("/is_friends", include("users.search.is_friends.urls")),
    path("/friends", include("users.search.friends.urls")),
    path("/verify_at", include("users.search.verify_at.urls")),
]