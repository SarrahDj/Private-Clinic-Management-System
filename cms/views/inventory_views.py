from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F
from django.db import transaction
from django.utils import timezone
from ..models.inventory import Inventory
from ..models.log import Log
from ..models.supplier import Supplier
from ..serializers.inventory import InventorySerializer

@api_view(['GET'])
def inventory_list(request):
    queryset = Inventory.objects.all()
    category = request.query_params.get('category', None)
    supplier = request.query_params.get('supplier', None)
    low_stock = request.query_params.get('low_stock', None)
    search = request.query_params.get('search', None)

    if category:
        queryset = queryset.filter(category_id=category)
    if supplier:
        queryset = queryset.filter(supplier_id=supplier)
    if low_stock:
        queryset = queryset.filter(stock_quantity__lte=F('reorder_level'))
    if search:
        queryset = queryset.filter(item_name__icontains=search)

    serializer = InventorySerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def inventory_create(request):
    serializer = InventorySerializer(data=request.data)
    if serializer.is_valid():
        inventory = serializer.save()
        Log.objects.create(
            inventory_id=inventory,
            quantity=inventory.stock_quantity,
            action='CREATE',
            date=timezone.now(),
            notes='Initial inventory creation'
        )
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            inventory = serializer.save()
            Log.objects.create(
                inventory_id=inventory,
                quantity=inventory.stock_quantity,
                action='UPDATE',
                date=timezone.now(),
                notes='Inventory details updated',
                item_name_backup=inventory.item_name,
                unit_backup=inventory.unit
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        try:
            with transaction.atomic():
                # Update all existing logs for this item with the backup name
                Log.objects.filter(inventory_id=inventory).update(
                    item_name_backup=inventory.item_name,
                    unit_backup=inventory.unit
                )
                
                # Create delete log entry
                Log.objects.create(
                    inventory_id=None,
                    quantity=inventory.stock_quantity,
                    action='DELETE',
                    date=timezone.now(),
                    notes=f"Item deleted from inventory",
                    item_name_backup=inventory.item_name,
                    unit_backup=inventory.unit
                )
                
                # Delete the inventory item
                inventory.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(f"Error during inventory deletion: {str(e)}")
            return Response(
                {'error': f'Failed to delete inventory: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def update_stock(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return Response(status=404)

    action = request.data.get('action')
    quantity = int(request.data.get('quantity', 0))
    purpose = request.data.get('purpose', '')
    supplier_data = request.data.get('supplier')

    if not quantity or quantity <= 0:
        return Response(
            {'error': 'Invalid quantity'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if action == 'increase':
        inventory.stock_quantity = F('stock_quantity') + quantity
        log_action = 'RESTOCK'
        
        if supplier_data:
            supplier, created = Supplier.objects.get_or_create(
                supplier_name=supplier_data['name'],
                defaults={
                    'phone_number': supplier_data['contact'],
                    'address_line': supplier_data.get('address', ''),
                }
            )
            inventory.supplier_id = supplier
    
    elif action == 'decrease':
        with transaction.atomic():
            inventory = Inventory.objects.select_for_update().get(pk=pk)
            if inventory.stock_quantity < quantity:
                return Response(
                    {'error': 'Insufficient stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            inventory.stock_quantity = F('stock_quantity') - quantity
            log_action = 'USAGE'
    
    else:
        return Response(
            {'error': 'Invalid action'},
            status=status.HTTP_400_BAD_REQUEST
        )

    inventory.save()
    inventory.refresh_from_db()

    # Create log with backup information
    Log.objects.create(
        inventory_id=inventory,
        supplier_id=inventory.supplier_id if action == 'increase' else None,
        quantity=quantity,
        action=log_action,
        date=timezone.now(),
        notes=purpose,
        item_name_backup=inventory.item_name,
        unit_backup=inventory.unit
    )

    serializer = InventorySerializer(inventory)
    response_data = serializer.data
    
    if inventory.stock_quantity <= inventory.min_stock:
        response_data['low_stock_alert'] = {
            'id': inventory.id,
            'item_name': inventory.item_name,
            'stock_quantity': inventory.stock_quantity,
            'unit': inventory.unit,
            'reorder_level': inventory.reorder_level
        }

    return Response(response_data)