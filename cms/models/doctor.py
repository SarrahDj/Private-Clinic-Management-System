from django.db import models

from .dep import Department
from .user import User

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_profiles')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    license_number = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    qualifications = models.TextField()
    years_of_experience = models.IntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField()  # 0 = Monday, 6 = Sunday
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_appointments = models.IntegerField()
    #is_surgery_day = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for Dr. {self.doctor.first_name} on day {self.day_of_week}"
