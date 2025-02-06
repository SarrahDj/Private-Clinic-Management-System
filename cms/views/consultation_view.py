from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Consultation, Prescription, Room, Patient, User
from ..serializers import (ConsultationSerializer, PrescriptionSerializer,
                         RoomSerializer, PatientSerializer, UserSerializer)

# Consultation Views
@api_view(['GET'])
def get_consultations(request):
    consultations = Consultation.objects.all()
    serializer = ConsultationSerializer(consultations, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
def get_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    serializer = ConsultationSerializer(consultation)
    return Response(serializer.data)

@api_view(['POST'])
def create_consultation(request):
    serializer = ConsultationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    serializer = ConsultationSerializer(consultation, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)