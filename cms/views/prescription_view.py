from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Prescription
from ..serializers import PrescriptionSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def create_prescription(request):
    """
    Create a new prescription.
    """
    serializer = PrescriptionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_prescription(request, pk):
    """
    Retrieve a specific prescription by ID.
    """
    try:
        prescription = Prescription.objects.get(pk=pk)
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)
    except Prescription.DoesNotExist:
        return Response({'error': 'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def retrieve_prescription_by_consultation(request, consultation_id):
    """
    Retrieve all prescriptions associated with a specific consultation.
    """
    try:
        prescriptions = Prescription.objects.filter(consultation_id=consultation_id)
        if not prescriptions.exists():
            return Response({'error': 'No prescriptions found for this consultation'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def retrieve_all_prescriptions(request):
    """
    Retrieve all prescriptions.
    """
    try:
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
def update_prescription(request, pk):
    """
    Update an existing prescription.
    """
    try:
        prescription = Prescription.objects.get(pk=pk)
        serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)  # Use partial=True for PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Prescription.DoesNotExist:
        return Response({'error': 'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['DELETE'])
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    prescription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)