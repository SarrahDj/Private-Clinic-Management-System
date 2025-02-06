from rest_framework import serializers
from ..models import Consultation
from ..serializers import PrescriptionSerializer

class ConsultationSerializer(serializers.ModelSerializer):

    doctor_first_name = serializers.CharField(source='doctor.first_name', read_only=True)
    doctor_last_name = serializers.CharField(source='doctor.last_name', read_only=True)
    patient_first_name = serializers.CharField(source='patient.first_name', read_only=True)
    patient_last_name = serializers.CharField(source='patient.last_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    class Meta:
        model = Consultation
        fields = '__all__'  # Include all fields