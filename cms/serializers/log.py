from rest_framework import serializers
from ..models.log import Log
from .supplier import SupplierSerializer
from .inventory import InventorySerializer

class LogSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(source='inventory_id', read_only=True)
    supplier = SupplierSerializer(source='supplier_id', read_only=True)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Handle item name for both existing and deleted items
        if instance.action == 'DELETE' and not instance.inventory_id:
            # For delete actions, use the backup name
            representation['inventory'] = {
                'item_name': instance.item_name_backup,
                'unit': 'units'  # Default unit for deleted items
            }
        elif not instance.inventory_id and instance.item_name_backup:
            # For other actions where the inventory item has been deleted
            # but we have the backup name
            representation['inventory'] = {
                'item_name': instance.item_name_backup,
                'unit': instance.unit_backup if hasattr(instance, 'unit_backup') else 'units'
            }
        
        # Only include supplier information for RESTOCK actions
        if instance.action != 'RESTOCK':
            representation['supplier'] = None
        
        return representation
    
    class Meta:
        model = Log
        fields = [
            'id',
            'inventory',
            'supplier',
            'quantity',
            'action',
            'date',
            'notes',
            'item_name_backup',
            'unit_backup'
        ]