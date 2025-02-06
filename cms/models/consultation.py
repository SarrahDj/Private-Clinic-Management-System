from django.db import models

from .dep import Room
from .patient import Patient
from .doctor import Doctor

class Consultation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultations')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='consultations')
    fee = models.CharField(max_length=100)
    def __str__(self):
        return f"Consultation {self.id} on {self.date}"

class Prescription(models.Model):
    consultation = models.ForeignKey('Consultation', on_delete=models.CASCADE, related_name='prescriptions' , null=True)

    medication = models.CharField(max_length=255)
    med_route = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    dosage_unit = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    frequency_unit = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    duration_unit = models.CharField(max_length=100)
    timing = models.CharField(max_length=100)
    prescribed_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription {self.id} - {self.medication}"
