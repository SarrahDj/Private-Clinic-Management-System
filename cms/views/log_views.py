from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from ..models.log import Log
from ..serializers.log import LogSerializer

@api_view(['GET'])
def log_list(request):
    try:
        # Use select_related to efficiently fetch related data
        queryset = Log.objects.select_related('inventory_id', 'supplier_id').all().order_by('-date')
        
        # Apply filters if provided
        action = request.query_params.get('action', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        search = request.query_params.get('search', None)

        if action:
            queryset = queryset.filter(action=action)

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        if search:
            queryset = queryset.filter(inventory_id__item_name__icontains=search)

        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )