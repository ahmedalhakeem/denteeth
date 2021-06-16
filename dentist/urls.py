from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_func, name="logout"),
    path('main', views.main, name="main"),
    path('add_patient', views.add_patient, name="add_patient"),
    path('all_patients', views.all_patients, name="all_patients"),
    path('patient/<int:patient_id>', views.patient, name="patient"),
    path("upcoming_appointments", views.upcoming_appointments, name="upcoming_appointments"),
    path("appointment", views.appointment, name="appointment"),
    path("change_appointment/<int:a_id>", views.change_appointment, name="change_appointment"),
    path("update_schedule", views.update_schedule, name="update_schedule"),
    path("archived", views.archived, name="archived"),
    path("search", views.search, name="search")
    
]