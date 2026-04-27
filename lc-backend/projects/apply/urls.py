from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.testView.as_view(), name="index"),
]