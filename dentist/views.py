from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from datetime import datetime
from django.urls import reverse


# Create your views here.
#login and the homepage
def index(request):
    if request.method == "POST":
        login_admin = Admin_Login(request.POST)
        if login_admin.is_valid():
            username = login_admin.cleaned_data['username']
            password = login_admin.cleaned_data['password']

            login_user = authenticate(request, username=username, password=password)
            if login_user is not None:
                login(request, login_user)
                return HttpResponseRedirect(reverse('main'))
            else:
                return HttpResponse('invalid login')
    else:
        if request.user.is_authenticated:
            return render(request, 'dentist/main.html')
        else:
            login_page = Admin_Login()
            return render(request, 'dentist/index.html',{
                "login_admin": login_page
        })
#Create logout function
def logout_func(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#create the main page
@login_required
def main(request):

    return render(request, 'dentist/main.html')
#create add_patient function
def add_patient(request):
    if request.method == "POST":
        # takes patient information from django forms
        patient = Add_Patient_form(request.POST or None)
        if patient.is_valid():
            name = patient.cleaned_data['name']
            age = patient.cleaned_data['age']
            gender = patient.cleaned_data['gender']
            contact = patient.cleaned_data['contact']
            
            #save it in the database
            new_patient = Patients(name=name, age=age, gender=gender, contact_number=contact)
            all_patients = Patients.objects.all()
            list = []
            for e in all_patients:
                list.append(e.name)
            print(list)
        
            if (new_patient.name in list):
                return render(request, 'dentist/add_patient.html',{
                    "message": "هذا الاسم تم ادخاله مسبقا في النظام"
                }) 
            else:
                new_patient.save()
                return HttpResponseRedirect(reverse('patient' ,args=(new_patient.pk,)))
    elif request.method=="GET":
        #all_patients = Patients.objects.values_list('name', flat=True)

        
        patient_form = Add_Patient_form()
        return render(request, "dentist/add_patient.html",{
            "patient_form" : patient_form
        })
# Display all patient names
def patients(request):
    patients = Patients.objects.all()
    return render(request, 'dentist/patients.html',{
        "patients": patients
    })

#show patient profile page
def patient(request, patient_id):
    patient = Patients.objects.get(pk=patient_id)
    #list all treatments for a particular patient
    treatments = Treatment.objects.filter(p_name=patient)
    print(treatments)
    
    return render(request, 'dentist/patient.html',{
        "patient": patient,
        "treatments": treatments
    })
# makes a new  appointment
def appointment(request):
    if request.method == "POST":

        app_form = Appointment(request.POST or None)
        if app_form.is_valid():
            patient_nam = app_form.cleaned_data["patient_name"]
            treatment_type = app_form.cleaned_data["treatment_type"]
            total_amount = request.POST['total_amount']
            notes = request.POST['notes']
            date = datetime.strptime(request.POST['appointment'], "%m/%d/%Y %H:%M")

            
            treatment = Treatment(p_name=patient_nam, treatments=treatment_type, total_cost=total_amount, notes=notes)
            treatment.save()
            
            ne_app = Next_appointment(patient_name=patient_nam, treatment=treatment, date=date, notes=notes)
            ne_app.save()
            #ne_app.save()
            return render(request, "dentist/appointments.html")
    
    else:
        return render(request, "dentist/appointments.html",{
            "form": Appointment()
        })
#Save appointment and total cost
def add_treatment(request, patient_id):
    patient = Patients.objects.get(pk=patient_id)
    if request.method == "POST":
        #procedure is saved in Treatment model
        procedure = request.POST['procedure']
        #Date id saved in pre-appointment model
        date = datetime.strptime(request.POST['date'], "%m/%d/%Y %H:%M")
        #total_cost is saved in Treatment model
        total_cost = int(request.POST["total_cost"])
        #Paid is saved in Pre-app model
        paid_amount = int(request.POST["paid_amount"])
        #note is saved in all model except Patient model
        notes = request.POST['notes']
        #remaining_amount is saved in patient model
        remaining_amount = int(total_cost - paid_amount)
        patient.remaining_amount = remaining_amount
        #Treatment model 
        new_treatment = Treatment(p_name=patient, treatment_procedure=procedure, total_cost=total_cost, notes=notes)
        if new_treatment is not None:
            new_treatment.save()
            patient.save()
            #saving pre-appointment
            pre_appointment = Previous_appointment(patient_name=patient, treatment=new_treatment, date=date, notes=notes, paid_amount=paid_amount)
            if pre_appointment is not None:
                pre_appointment.save()

                return HttpResponseRedirect(reverse('patient', args=(patient_id,)))
        else:
            return HttpResponse('this treatment cannot be saved!') 


def next_appointment(request):
    next_appointments = Next_appointment.objects.all()
    if next_appointments.exists():
        return render(request, "dentist/next_appointment.html",{
            "next_appointment": next_appointments
        })
    else:
    
        return render(request, "dentist/next_appointment.html",{
            "message" : "No upcoming appointments"
        }) 