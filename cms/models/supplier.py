from django.db import models

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.supplier_name}"