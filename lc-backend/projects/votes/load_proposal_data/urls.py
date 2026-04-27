from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:proposal_id>", views.load_candidates.as_view(), name="load_candidates"),
]