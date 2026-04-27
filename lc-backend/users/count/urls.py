from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.view.as_view())
]