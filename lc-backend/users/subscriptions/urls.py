from django.urls import include, path

from . import views

urlpatterns = [
    path("/create_subscription", include("users.subscriptions.create_subscription.urls")),
    path("/delete_subscription", include("users.subscriptions.delete_subscription.urls")),
]