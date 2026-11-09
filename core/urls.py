from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("resources/", views.resources, name="resources"),
    path("resources/subscribe/", views.subscribe, name="subscribe"),
    path("privacy/", views.privacy, name="privacy"),
]
