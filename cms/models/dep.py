from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.department_name


class Room(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.IntegerField()
    room_number = models.IntegerField(unique=True)
    type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} in {self.department.department_name}"
