from django.db import models
from .inventory import Inventory
from .supplier import Supplier

class Log(models.Model):
    inventory_id = models.ForeignKey(
        Inventory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    supplier_id = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    quantity = models.IntegerField()
    action = models.CharField(max_length=20)
    date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
    item_name_backup = models.CharField(max_length=255, null=True, blank=True)
    unit_backup = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-date']