from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Patient, MedicalHistory, MedicalRecord
from ..serializers import MedicalRecordSerializer


@api_view(['GET'])
def get_patient_medical_records(request, patient_id):
    """
    Retrieve all medical records for a specific patient
    """
    try:
        # Verify patient exists
        patient = get_object_or_404(Patient, id=patient_id)

        # Get or create medical history for the patient
        medical_history, _ = MedicalHistory.objects.get_or_create(patient=patient)

        # Fetch records for this medical history
        records = MedicalRecord.objects.filter(history=medical_history)

        # Serialize the records
        serializer = MedicalRecordSerializer(records, many=True)

        return Response({
            'patient_id': patient.id,
            'patient_name': f"{patient.first_name} {patient.last_name}",
            'medical_records': serializer.data
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def create_medical_record(request, patient_id):
    """
    Create a new medical record for a specific patient
    """
    try:
        # Verify patient exists
        patient = get_object_or_404(Patient, id=patient_id)

        # Get or create medical history for the patient
        medical_history, _ = MedicalHistory.objects.get_or_create(patient=patient)

        # Prepare data for serialization
        record_data = request.data.copy()
        record_data['history'] = medical_history.id
        record_data['created_by'] = request.user.id

        # Validate and save the record
        serializer = MedicalRecordSerializer(data=record_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
def update_medical_record(request, record_id):
    """
    Update an existing medical record
    """
    try:
        # Get the existing record
        record = get_object_or_404(MedicalRecord, id=record_id)

        # Prepare update data
        update_data = request.data.copy()
        update_data['updated_by'] = request.user.id

        # Validate and save the updated record
        serializer = MedicalRecordSerializer(record, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def delete_medical_record(request, record_id):
    """
    Delete a medical record
    """
    try:
        # Get the record
        record = get_object_or_404(MedicalRecord, id=record_id)

        # Delete the record
        record.delete()

        return Response(
            {'message': 'Medical record deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )