from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.book_trial, name="book"),
    path("thanks/", views.thanks, name="thanks"),
]
