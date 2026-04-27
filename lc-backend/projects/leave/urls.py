from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:project_id>/<str:user_id>", views.testView.as_view()),
]