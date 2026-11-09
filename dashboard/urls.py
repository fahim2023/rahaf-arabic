from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.questions, name="questions"),
    path("questions/<int:pk>/", views.answer, name="answer"),
    path("questions/<int:pk>/delete/", views.delete_question, name="delete_question"),
    path("bookings/", views.bookings, name="bookings"),
    path("bookings/<int:pk>/", views.update_booking, name="update_booking"),
    path("students/", views.students, name="students"),
    path("students/<int:pk>/", views.student_detail, name="student"),
    path("students/<int:pk>/<str:kind>/<int:item_pk>/", views.student_item, name="student_item"),
    path("invites/<int:pk>/delete/", views.delete_invite, name="delete_invite"),
]
