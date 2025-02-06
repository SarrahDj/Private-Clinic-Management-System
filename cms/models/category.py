from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.category_name}"