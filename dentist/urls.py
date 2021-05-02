from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_func, name="logout"),
    path('main', views.main, name="main"),
    path('add_patient', views.add_patient, name="add_patient"),
    path('patients', views.patients, name="patients"),
    path('patient/<int:patient_id>', views.patient, name="patient"),
    path('add_treatment/<int:patient_id>', views.add_treatment, name="add_treatment"),
    path("next_appointment", views.next_appointment, name="next_appointment"),
    path("appointment", views.appointment, name="appointment"),
    path("modify_appointment/<int:a_id>", views.modify_appointment, name="modify_appointment")
]