from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from django.shortcuts import get_object_or_404
from ..serializers.A_appointment import AappointmentSerializer
from ..models import Appointment
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def appointment_list(request):
    if request.method == 'GET':
        appointments = Appointment.objects.select_related(
            'doctor', 'department_id', 'room'
        ).all()
        serializer = AappointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            logger.info(f"Received appointment data: {request.data}")
            serializer = AappointmentSerializer(data=request.data)
            
            if serializer.is_valid():
                logger.info("Data validated successfully")
                appointment = serializer.save()
                
                # Fetch the created appointment with all related fields
                created_appointment = Appointment.objects.select_related(
                    'doctor', 'department_id', 'room'
                ).get(id=appointment.id)
                
                response_serializer = AappointmentSerializer(created_appointment)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Unexpected error in appointment_list: {str(e)}")
            return Response(
                {"detail": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PUT', 'DELETE'])
def appointment_detail(request, pk):
    """
    Retrieve, update or delete an appointment.
    """
    try:
        # Get the appointment with related fields
        appointment = Appointment.objects.select_related(
            'doctor', 'department_id', 'room'
        ).get(pk=pk)
    except Appointment.DoesNotExist:
        logger.error(f"Appointment with id {pk} not found")
        return Response(
            {"error": "Appointment not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        try:
            serializer = AappointmentSerializer(appointment)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving appointment details: {str(e)}")
            return Response(
                {"error": f"Error retrieving appointment details: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'PUT':
        try:
            logger.info(f"Updating appointment {pk} with data: {request.data}")
            
            # Create a mutable copy of the data
            data = request.data.copy()
            
            # Convert emergency_level to integer if it's a string
            if 'emergency_level' in data and isinstance(data['emergency_level'], str):
                data['emergency_level'] = int(data['emergency_level'])

            serializer = AappointmentSerializer(
                appointment, 
                data=data, 
                partial=True
            )
            
            if serializer.is_valid():
                # Save the updated appointment
                updated_appointment = serializer.save()
                
                # Fetch the updated appointment with all related fields
                refreshed_appointment = Appointment.objects.select_related(
                    'doctor', 'department_id', 'room'
                ).get(id=updated_appointment.id)
                
                response_serializer = AappointmentSerializer(refreshed_appointment)
                logger.info(f"Successfully updated appointment {pk}")
                return Response(response_serializer.data)
            else:
                logger.error(f"Validation errors while updating appointment: {serializer.errors}")
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"Error updating appointment: {str(e)}")
            return Response(
                {"error": f"Error updating appointment: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'DELETE':
        try:
            # Get appointment details before deletion for logging
            appointment_info = {
                'id': appointment.id,
                'patient_name': appointment.patient_full_name,
                'start_time': appointment.start_time
            }
            
            # Delete the appointment
            appointment.delete()
            
            logger.info(f"Successfully deleted appointment: {appointment_info}")
            return Response(
                {"message": "Appointment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error(f"Error deleting appointment: {str(e)}")
            return Response(
                {"error": f"Error deleting appointment: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Optional: Add a function to cancel appointment
@api_view(['POST'])
def cancel_appointment(request, pk):
    """
    Cancel an appointment instead of deleting it
    """
    try:
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = "Cancelled"
        appointment.save()
        
        serializer = AappointmentSerializer(appointment)
        logger.info(f"Successfully cancelled appointment {pk}")
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error cancelling appointment: {str(e)}")
        return Response(
            {"error": f"Error cancelling appointment: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )