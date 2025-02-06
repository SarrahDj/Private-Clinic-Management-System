from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from django.shortcuts import get_object_or_404
from ..models.surgery import Surgery, Surgery_Type
from ..models.doctor import Doctor
from ..serializers.W_surgery import WSurgerySerializer, SurgeryTypeDetailSerializer

@api_view(['GET'])
def get_surgeries(request, doctor_id):
    if not doctor_id:
        return Response(
            {"error": "Doctor ID is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Filter surgeries by primary surgeon
    upcoming_surgeries = Surgery.objects.filter(
        ~Q(status='Completed'),
        primary_surgeon_id=doctor_id
    ).order_by('schedules_start_time')
    
    completed_surgeries = Surgery.objects.filter(
        status='Completed',
        primary_surgeon_id=doctor_id
    ).order_by('-schedules_start_time')

    upcoming_serializer = WSurgerySerializer(upcoming_surgeries, many=True)
    completed_serializer = WSurgerySerializer(completed_surgeries, many=True)

    return Response({
        'upcoming': upcoming_serializer.data,
        'completed': completed_serializer.data
    })

@api_view(['POST'])
def schedule_surgery(request):
    try:
        primary_surgeon_id = request.data.get('primary_surgeon')
        surgery_type_id = request.data.get('surgery_type')
        
        # Get the surgery type to access its department
        surgery_type = Surgery_Type.objects.get(id=surgery_type_id)
        
        # Prepare surgery data with department
        surgery_data = {
            'patient_full_name': request.data.get('patient_full_name'),
            'surgery_type': surgery_type_id,
            'department': surgery_type.department.id,  # Add department ID
            'primary_surgeon': primary_surgeon_id,
            'schedules_start_time': request.data.get('schedules_start_time'),
            'schedules_end_time': request.data.get('schedules_end_time'),
            'pre_op_notes': request.data.get('pre_op_notes'),
            'status': 'Scheduled'
        }
        
        serializer = WSurgerySerializer(data=surgery_data)
        if serializer.is_valid():
            surgery = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Surgery_Type.DoesNotExist:
        return Response(
            {"error": "Surgery type not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def complete_surgery(request, surgery_id):
    try:
        surgery = Surgery.objects.get(id=surgery_id)
        
        # Update surgery with completion data
        completion_data = {
            'status': 'Completed',
            'post_op_notes': request.data.get('post_op_notes'),
            'complications': request.data.get('complications'),
            'actual_end_time': datetime.now()
        }
        
        serializer = WSurgerySerializer(
            surgery,
            data=completion_data,
            partial=True  # Allow partial updates
        )
        
        if serializer.is_valid():
            updated_surgery = serializer.save()
            return Response(
                WSurgerySerializer(updated_surgery).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Surgery.DoesNotExist:
        return Response(
            {"error": "Surgery not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(['GET'])
def get_surgery_type_details(request, type_id):
    """
    Get detailed information about a specific surgery type.
    """
    try:
        surgery_type = get_object_or_404(Surgery_Type, id=type_id)
        serializer = SurgeryTypeDetailSerializer(surgery_type)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
