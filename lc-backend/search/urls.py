from django.urls import path

from . import views

urlpatterns = [
    path("<str:query>/<str:stringified_search_parameters>", views.testView.as_view(), name="index"),
]