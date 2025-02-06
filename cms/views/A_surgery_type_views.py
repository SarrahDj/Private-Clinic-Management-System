from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from ..models.surgery import Surgery_Type
from ..serializers.A_surgery import ASurgeryTypeSerializer

@api_view(['POST'])
def create_surgery_type(request):
    """
    Create a new surgery type
    """
    serializer = ASurgeryTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_surgery_types(request):
    """
    Get all surgery types
    """
    surgery_types = Surgery_Type.objects.all()
    serializer = ASurgeryTypeSerializer(surgery_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_surgery_types_by_department(request, department_id):
    """
    Get surgery types filtered by department
    """
    surgery_types = Surgery_Type.objects.filter(department_id=department_id)
    serializer = ASurgeryTypeSerializer(surgery_types, many=True)
    return Response(serializer.data)