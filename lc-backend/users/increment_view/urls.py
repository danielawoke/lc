from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:entry_id>", views.view.as_view()),
]   