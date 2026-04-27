from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:proposal_id>", views.view.as_view()),
]