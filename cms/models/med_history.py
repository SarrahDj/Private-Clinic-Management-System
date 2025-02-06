from django.db import models

from .patient import Patient
from .user import User

class MedicalRecord(models.Model):
    history = models.ForeignKey('MedicalHistory', on_delete=models.SET_NULL, null=True, related_name='medical_records')
    record_type = models.CharField(max_length=100)
    record_date = models.DateTimeField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    is_confidential = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_medical_records')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_medical_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record {self.id} - {self.record_type}"


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"History for {self.patient}"


