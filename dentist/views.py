import json
from django.shortcuts import render
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
def all_patients(request):
    patients = Patients.objects.all()
    return render(request, 'dentist/patients.html',{
        "patients": patients
    })

#show patient profile page
def patient(request, patient_id):
    patient = Patients.objects.get(pk=patient_id)
    #list all treatments for a particular patient
    # treatments = Treatment.objects.filter(p_name=patient) //remove
    return render(request, 'dentist/patient.html',{
        "patient": patient
    })

# make a new  appointment
def appointment(request):
    if request.method == "POST":

        app_form = Appointment(request.POST or None)
        if app_form.is_valid():
            patient_name = app_form.cleaned_data["patient_name"]
            treatment_type = app_form.cleaned_data["treatment_type"]
            # total_amount = request.POST['total_amount']
            notes = request.POST['notes']
            date = datetime.strptime(request.POST['appointment'], "%m/%d/%Y %H:%M")

            # Save the treatment and type of medication as well as the cost of medication 
            treatment = Treatment(p_name=patient_name, treatments=treatment_type,notes=notes)
            if treatment:
                treatment.save()
            else:
                return HttpResponse({'msg': "no treatment was added"})
            #extract the person whose its name is /patient_name/


            patient_id = treatment.p_name.id
            patient = Patients.objects.get(pk=patient_id)
            # extract the amount of treatment and add it to the remaining amount of the patient
            cost = treatment.treatments.total_cost
            patient.remaining_amount += int(cost)
            patient.save()
            #print(patient.name)
        
            
            # now, we can make a new appointment for this particular patient
            new_appointment = Next_appointment(patient_name=patient_name, treatment=treatment, date=date, notes=notes)
            new_appointment.save()
            #ne_app.save()
            return HttpResponseRedirect(reverse('next_appointment'))
    
    else:
        return render(request, "dentist/appointments.html",{
            "form": Appointment()
        })

#Save appointment and total cost
def add_treatment(request, patient_id):
    return
    # patient = Patients.objects.get(pk=patient_id)
    # # medication list 
    # mediction_list = Medication_list.objects.all()
    # if request.method == "POST":
    #     #procedure is saved in Treatment model
    #     procedure = request.POST['procedure']
    #     #Date id saved in pre-appointment model
    #     date = datetime.strptime(request.POST['date'], "%m/%d/%Y %H:%M")
    #     #total_cost is saved in Treatment model
    #     total_cost = int(request.POST["total_cost"])
    #     #Paid is saved in Pre-app model
    #     paid_amount = int(request.POST["paid_amount"])
    #     #note is saved in all model except Patient model
    #     notes = request.POST['notes']
    #     #remaining_amount is saved in patient model
    #     remaining_amount = int(total_cost - paid_amount)
    #     patient.remaining_amount = remaining_amount
    #     #Treatment model 
    #     new_treatment = Treatment(p_name=patient, treatments=procedure, total_cost=total_cost, notes=notes)
    #     if new_treatment is not None:
    #         new_treatment.save()
    #         patient.save()
    #         #saving pre-appointment
    #         pre_appointment = Previous_appointment(patient_name=patient, treatment=new_treatment, date=date, notes=notes, paid_amount=paid_amount)
    #         if pre_appointment is not None:
    #             pre_appointment.save()

    #             return HttpResponseRedirect(reverse('patient', args=(patient_id,)))
    #     else:
    #         return HttpResponse('this treatment cannot be saved!') 

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
            "message" : "No upcoming appointments"
        }) 
    
# Change the currnet appointment    
def change_appointment(request, a_id):
    new_appointment = Next_appointment.objects.get(pk=a_id)
    patient_names = Patients.objects.all()
    treatments = Treatment.objects.all()
    
    
    print(new_appointment)
    if request.method == 'POST':
        #name = request.POST['name']
        #treatment =request.POST['treatment']
        date = datetime.strptime(request.POST['date'], "%m/%d/%Y %H:%M")
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
        print(id)
        name = data['name']
        treatment = data['treatment']
        date= data['date']
        notes = data['notes']
        paid_amount = data['paid_amount']
        


        #Delete this record from the Next appointment table
        omitted_record = Next_appointment.objects.get(pk = id)
        patient_id = omitted_record.patient_name.id 
        patient = Patients.objects.get(pk=patient_id)
        # archive this appointment
        new_appointment = Next_appointment(patient_name=patient, treatment=treatment, date= date, notes=notes)
        new_appointment.save()
        # Archive the current appointment and save it 
        archived_appointment = Previous_appointment(patient_name= omitted_record.patient_name, treatment=omitted_record.treatment, date= omitted_record.date, 
        notes= omitted_record.notes, paid_amount=paid_amount)
        archived_appointment.save()
        # previous = Previous_appointment(patient_name= name, treatment= treatment, date=date, )
        
        patient.remaining_amount -= int(paid_amount)
        patient.save()
        print(f"id={patient_id}")
        # print(omitted_record)
        print(paid_amount)
        # omitted_record.delete()
        #archive this particular recodrd. Save it in the previous appointment
        

        return JsonResponse({"message": "successful"})
    return JsonResponse({"message": "failed"})

#when the user press archive button on the modal form
@csrf_exempt
def archived(request):
    if request.method == "POST":
        data= json.loads(request.body)
        id = data['id']
        paid_amount = data['paid_amount']
        #select this record so that it will be archived to the previous appointment
        record = Next_appointment.objects.get(pk=id)
        #Archive this appointment
        # get the patient from DB
        patient_id = record.patient_name.id
        patient = Patients.objects.get(pk=patient_id)
        patient.remaining_amount -= int(paid_amount)
        patient.save()
        print(patient.remaining_amount)
       
        #  get the debit amount  and subtract paid_amount from the remaining amount
        # patient.remaining_amount  -= int(paid_amount)
        # patient.save()
        
        # print(debit_amount)
        archived_record = Previous_appointment(patient_name=record.patient_name, treatment = record.treatment, date= record.date, notes= record.notes, paid_amount = paid_amount )
        archived_record.save()
        record.delete()
        # print(record.treatment.total_cost)
        
        # record.save() 
        # print(record.treatment.total_cost)

        print(id)

    
        return JsonResponse({"message": "successful"})
    return JsonResponse({"msg": "Failed"})
def modal(request):
    return render(request, "dentist/modal.html")



 