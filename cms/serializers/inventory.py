from rest_framework import serializers
from ..models.inventory import Inventory
from .supplier import SupplierSerializer
from .category import CategorySerializer

class InventorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='category_id', read_only=True)
    supplier = SupplierSerializer(source='supplier_id', read_only=True)
    low_stock_alert = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'item_name', 'description', 'category', 'supplier', 
            'stock_quantity', 'min_stock', 'unit', 'reorder_level', 
            'purchase_price', 'expiry_date', 'category_id', 'supplier_id',
            'low_stock_alert'
        ]

    def get_low_stock_alert(self, obj):
        """
        Returns low stock alert information if stock is at or below reorder level
        """
        if obj.stock_quantity <= obj.reorder_level:
            return {
                'id': obj.id,
                'item_name': obj.item_name,
                'stock_quantity': obj.stock_quantity,
                'unit': obj.unit,
                'reorder_level': obj.reorder_level
            }
        return None