import json
import re
from django.db.models import query
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from datetime import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


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
@login_required()
def add_patient(request):
    if request.method == "POST":
        # takes patient information from django forms
        patient = Add_Patient_form(request.POST or None)
        if patient.is_valid():
            name = patient.cleaned_data['name']
            age = patient.cleaned_data['age']
            gender = patient.cleaned_data['gender']
            contact = patient.cleaned_data['contact']
            
            #Create a new patient 
            new_patient = Patients(name=name, age=age, gender=gender, contact_number=contact)
            # check if this newly created patient is already existed in the DB.
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
@login_required()
def all_patients(request):
    patients = Patients.objects.all()
    # add pagination
    paginator = Paginator(patients, 3)
    page_number= request.GET.get('page')
    pages = paginator.get_page(page_number)

    return render(request, 'dentist/patients.html',{
        "patients": patients,
        "pages": pages
    })

#show patient profile page
@login_required()
def patient(request, patient_id):
    patient = Patients.objects.get(pk=patient_id)
    old_appointments = Previous_appointment.objects.filter(patient_name=patient).order_by('-date')
    next_appointmens = Next_appointment.objects.filter(patient_name=patient)
    treatment = Treatment.objects.filter(p_name=patient).order_by('-date_created')
    for item in treatment:
        print(item.paid_amount)

    if  not next_appointmens:
        return render(request, 'dentist/patient.html',{
            "patient": patient,
            "message" : "لا توجد مراجعات قادمة",
            "old_appointments": old_appointments,
            "treatment" : treatment
        })
    else:
        return render(request, 'dentist/patient.html',{
            "patient": patient,
            "old_appointments": old_appointments,
            "next_appointments": next_appointmens,
            "treatment" : treatment
    })

# make a new  appointment
@login_required()
def appointment(request):
    if request.method == "POST":

        app_form = Appointment(request.POST or None)
        if app_form.is_valid():
            patient_name = app_form.cleaned_data["patient_name"]
            treatment_type = app_form.cleaned_data["treatment_type"]
            notes = request.POST['notes']
            date = datetime.strptime(request.POST['appointment'], "%Y-%m-%dT%H:%M")
            paid_amount = request.POST['paid_amount']
            remaining_amount = request.POST['remaining_amount']
            patient = Patients.objects.get(name=patient_name)
           

            # Save the treatment and type of medication as well as the cost of medication 
            treatment = Treatment(p_name=patient, treatments=treatment_type,notes=notes, paid_amount=paid_amount)
            if treatment:
                treatment.save()
            else:
                return HttpResponse({'msg': "no treatment was added"})
            patient_id = treatment.p_name.id
            patient = Patients.objects.get(pk=patient_id)
            patient.remaining_amount = remaining_amount
            patient.save()

            # now, we can make a new appointment for this particular patient
            new_appointment = Next_appointment(patient_name=patient, treatment=treatment, date=date, notes=notes)
            all_appointments = Next_appointment.objects.all()
            list = []
            # for apo in all_appointments:
            for e in all_appointments:
                list.append(e.date)
            if (new_appointment.date in list):
                return render(request, "dentist/appointments.html",{
                    "message" : "this time is already booked"
                })
            else:
                new_appointment.save()
                return HttpResponseRedirect(reverse('upcoming_appointments'))
    
    else:
        patients = Patients.objects.all()
        print(patients)
        return render(request, "dentist/appointments.html",{
            "form": Appointment(),
            'patients': patients,
        })

@login_required
def upcoming_appointments(request):
    upcoming_appointments = Next_appointment.objects.all().order_by('date')
    #medlist = Medication_list.objects.all()
    if upcoming_appointments.exists():
        return render(request, "dentist/upcoming_appointments.html",{
            "upcoming_appointments": upcoming_appointments,
            #"medlist" : medlist
        })
    else:
    
        return render(request, "dentist/upcoming_appointments.html",{
            "message" : "لا يوجد مواعيد قادمة"
        }) 
    
# Change the currnet appointment    
def change_appointment(request, a_id):
    new_appointment = Next_appointment.objects.get(pk=a_id)
    patient_names = Patients.objects.all()
    treatments = Treatment.objects.all()
    
    
    print(new_appointment)
    if request.method == 'POST':
        date = datetime.strptime(request.POST['date'], "%Y-%m-%dT%H:%M")
        # date = datetime.strptime(request.POST['date'], "%m/%d/%Y %H:%M")
        notes = request.POST['notes']

        
       
        new_appointment.date = date
        new_appointment.notes = notes
        new_appointment.save()
        return HttpResponse('The appointment has been changed successfully')
    else:
        return render(request, "dentist/change_appointment.html",{
            "edit_app" : new_appointment,

            "patients" : patient_names,
            "treatments" : treatments
        })


# the user can make a new appointment and 
@csrf_exempt
def update_schedule(request):
    if request.method == "POST":
        data =  json.loads(request.body)
        id = data['id']
        name = data['name']
        treatment = data['treatment']
        date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M")
        notes = data['notes']
        # paid_amount = data['paid_amount']
        # remaining_amount = data['remaining_amount']
        #Delete this record from the Next appointment table###.
        omitted_record = Next_appointment.objects.get(pk = id)
        # extract  the patient## 
        patient_id = omitted_record.patient_name.id 
        patient = Patients.objects.get(pk=patient_id)
        #extract the treatement###
        treatment_id = omitted_record.treatment.id
        treatment_name = Treatment.objects.get(pk=treatment_id)
        
        # added_cost = treatment_name.treatments.total_cost
        
        # archive this appointment
        new_appointment = Next_appointment(patient_name=patient, treatment=treatment_name, date= date, notes=notes)
        new_appointment.save()
        # Archive the current appointment and save it 
        archived_appointment = Previous_appointment(patient_name= omitted_record.patient_name, treatment=omitted_record.treatment, date= omitted_record.date, 
        notes= omitted_record.notes)
        archived_appointment.save()
        print(f"id={patient_id}")
        # print(omitted_record)
        #  print(paid_amount)
        omitted_record.delete()
        #archive this particular recodrd. Save it in the previous appointment

        return JsonResponse({"message": "successful"})
    return JsonResponse({"message": "failed"})

#when the user press archive button on the modal form
@csrf_exempt
def archived(request):
    if request.method == "POST":
        data= json.loads(request.body)
        id = data['id']
        treatment_type = data['treatment_type']
        record = Next_appointment.objects.get(pk=id)
        # Get the patient information 
        patient_id = record.patient_name.id
        patient = Patients.objects.get(pk=patient_id)
        # Get the treatment information
        treatment_id = record.treatment.id
        treatment = Treatment.objects.get(pk=treatment_id)
        # check the price of a particular treatment
        med_type = Medication_list.objects.get(treatment_title=treatment_type)
        print(med_type)
        # patient.remaining_amount -= med_type.total_cost
        # patient.save()
        # archive this record
        archive_appointment = Previous_appointment(patient_name=record.patient_name, treatment=record.treatment, date=record.date, notes=record.notes)
        archive_appointment.save()
        record.delete()

    
        return JsonResponse({"message": "successful"})
    return JsonResponse({"msg": "Failed"})

#  Search function 
def search(request):
    context_dict ={}
    if request.method == "GET":
        query = request.GET.get('search')
        results = Patients.objects.filter(name__icontains=query)
        if results.count():
            context_dict['results'] = results
        else:
            context_dict['no_results'] = query
    
    return render(request, "dentist/search.html",{
        "context_dict": context_dict
    })
def add_treatment(request):
    if request.method == "POST":
        treatment_title = request.POST['treatment_title']
        new_med_treatment = Medication_list(treatment_title=treatment_title)
        new_med_treatment.save()
        return HttpResponseRedirect(reverse('appointment'))

   


 