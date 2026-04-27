from django.urls import include, path

from . import views

urlpatterns = [
    path("/load_personal_settings", include("users.settings.load_personal_settings.urls"), name="load_personal_settings"),
    path("/update_personal_settings", include("users.settings.update_personal_settings.urls")),
    path("/update_notification_settings", include("users.settings.update_notification_settings.urls")),
]