from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>/<str:relation>", views.testView.as_view()),
]