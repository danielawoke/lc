from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>", views.updatePersonalSettings.as_view(), name="update_personal_settings"),
]