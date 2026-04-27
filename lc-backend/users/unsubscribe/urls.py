from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>", views.testView.as_view()),
]