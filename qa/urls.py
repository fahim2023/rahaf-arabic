from django.urls import path

from . import views

app_name = "qa"

urlpatterns = [
    path("", views.question_list, name="list"),
    path("ask/", views.ask, name="ask"),
]
