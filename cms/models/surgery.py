from django.db import models

from ..models.doctor import Doctor
from ..models.dep import Room , Department

class Surgery_Type(models.Model):
    type_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    typical_duration_min = models.IntegerField(blank=False, null=False)
    preparation_instructions = models.TextField(blank=True, null=True)
    recovery_instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Type: {self.type_name}"

class Surgery(models.Model):
    
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Pre-Op', 'Pre-Op'),
        ('In Surgery', 'In Surgery'),
        ('Post-Op', 'Post-Op'),
        ('Recovery', 'Recovery'),
        ('Completed', 'Completed'),
    ]
    
    patient_full_name = patient_full_name = models.CharField( default = "patient full name" ,max_length=255)
    primary_surgeon = models.ForeignKey(Doctor, on_delete=models.CASCADE ,  null=True, related_name='surgeries', blank=True)
    surgery_type = models.ForeignKey(Surgery_Type, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    operating_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='surgeries', blank=True)
    schedules_start_time = models.DateTimeField()
    schedules_end_time = models.DateTimeField(null=True)
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    pre_op_notes = models.TextField(blank=True, null=True)
    post_op_notes = models.TextField(blank=True, null=True)
    complications = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled'
    )
    
    def __str__(self):
        return (
            f"Surgery: {self.surgery_type} | Patient: {self.patient_full_name} | "
            f"Surgeon: {self.primary_surgeon} | Room: {self.operating_room} | "
            f"schedules: {self.schedules_start_time} - {self.schedules_end_time}"
        )
        