from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>/<str:application_id>", views.view.as_view())
]