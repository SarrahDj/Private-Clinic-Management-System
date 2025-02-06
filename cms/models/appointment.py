from django.db import models

from ..models.doctor import Doctor
from ..models.user import User
from ..models.dep import Room , Department


class Appointment(models.Model):

    patient_full_name = models.CharField( default = "Patient full name" ,max_length=255)
    patient_address = models.TextField(default="Default Address")
    patient_phone_number = models.CharField(max_length=10 , default= "0000")
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE ,  null=True, related_name='appointments', blank=True)
    is_emergency = models.BooleanField(default=False)
    emergency_level = models.IntegerField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='appointments', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_appointments')

    def __str__(self):
        return f"Appointment {self.id} - {self.status}"

    def cancel(self):
        self.status = "Cancelled"
        self.save()