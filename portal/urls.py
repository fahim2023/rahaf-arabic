from django.urls import path

from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("homework/<int:pk>/toggle/", views.toggle_homework, name="toggle_homework"),
    path("files/<int:pk>/", views.download, name="download"),
]
