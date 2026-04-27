from django.urls import include, path

from . import views

urlpatterns = [
    path("/<str:user_id>/<str:receiver_tag>", views.testView.as_view()),
]