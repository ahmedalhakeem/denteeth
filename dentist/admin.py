from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patients)
admin.site.register(Treatment)
admin.site.register(Previous_appointment)
admin.site.register(Next_appointment)
admin.site.register(Medication_list)
