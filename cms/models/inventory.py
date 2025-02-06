from django.db import models

from .category import Category
from .supplier import Supplier

class Inventory(models.Model):
    item_name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='categories')
    supplier_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='suppliers')
    stock_quantity = models.IntegerField()
    min_stock = models.IntegerField()
    unit = models.CharField(max_length=20)
    reorder_level = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.item_name}"