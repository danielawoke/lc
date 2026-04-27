from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>", views.testView.as_view(), name="index"),
]