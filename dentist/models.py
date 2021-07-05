from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Create your models here.
class User(AbstractUser):
    pass
class Patients(models.Model):
    male = "m"
    female = "f"
    gender_type = [
        (male, "m"),
        (female, "f")
    ]
    name = models.CharField(max_length=64)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=2, choices=gender_type, default=female, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    remaining_amount = models.IntegerField(default=0) 
    date_created = models.DateTimeField(auto_now_add=True)
    #appointment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='patient_treat')

    def __str__(self):
        return f"{self.name}"
class Medication_list(models.Model):
    treatment_title = models.CharField(max_length=100)
    # total_cost = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.treatment_title}"
    

class Treatment(models.Model):
    p_name= models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="patient_name")
    treatments = models.ForeignKey(Medication_list, on_delete=models.CASCADE, related_name="list", null=True, blank=True)
    status= models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=100, default="")
    paid_amount = models.IntegerField(default=0)
   

    def __str__(self):
        return f"{self.treatments}"

class Next_appointment(models.Model):
    patient_name = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="np_name")
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="n_treatment")
    date = models.DateTimeField(auto_now=False, auto_now_add=False, default=None)
    notes = models.CharField(max_length=100, default="")

class Previous_appointment(models.Model):
    patient_name = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="pp_name")
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="p_treatment")
    date = models.DateTimeField(auto_now=False, auto_now_add=False, default=None)
    notes = models.CharField(max_length=100, default="")
    # paid_amount = models.IntegerField(default=0)

    def serialize(self):
        return{
            "id": self.id,
            "patient_name": self.patient_name.name,
            "date": self.date.strftime("%m/%d/%Y %H:%M"),
            "note": self.notes,
            "paid_amount" : self.paid_amount

        }
    





