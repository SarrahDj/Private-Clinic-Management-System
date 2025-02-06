from django.db import models

class Staff(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='staff_profiles')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='staff_roles')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    license_number = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.ForeignKey('Specialty', on_delete=models.SET_NULL, null=True, related_name='staff_specialties')
    qualifications = models.TextField(blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    available_for_surgery = models.BooleanField(default=False)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='staff_department')
    shift_preference = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role.role_name})"
