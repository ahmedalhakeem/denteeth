from django import forms
from django.forms import ModelForm
from dentist.models import User
from .models import *
import datetime
#from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

class Admin_Login(forms.Form):
    username= forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Username"}))
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"}))


class Add_Patient_form(forms.Form):
    male = "m"
    female = "f"
    gender_type = [
        (male, "m"),
        (female, "f")
    ]
    name = forms.CharField(label="الاسم", required=True, widget=forms.TextInput(attrs={"class": "inputForm", "placeholder": "ادخل اسم المريض..."}))
    age = forms.CharField(label="العمر", required=False, widget=forms.NumberInput(attrs={"class": "inputForm", "placeholder": "ادخل عمر المريض..."}))
    gender = forms.ChoiceField(label="الجنس",choices=gender_type, widget=forms.Select(attrs={"class": "inputForm",}))
    contact = forms.CharField(label="رقم الموبايل", required=True, widget=forms.NumberInput(attrs={"class": "inputForm", "placeholder": "ادخل رقم الموبايل..."}))

class Appointment(forms.Form):
    #class Meta:
        #model = Next_appointment
        #fields = ['patient_name', 'treatment', 'date', 'notes']
    patient_name = forms.ModelChoiceField(required=True,label="اختر المريض",widget=forms.Select(attrs={"class": "form-control"}), queryset=Patients.objects.all())
    treatment_type = forms.ModelChoiceField(required=True,label="اختر نوع العلاج", widget=forms.Select(attrs={"class": "inputForm"}) ,queryset=Medication_list.objects.all())
    