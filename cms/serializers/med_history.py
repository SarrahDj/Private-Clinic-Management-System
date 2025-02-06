from rest_framework import serializers
from ..models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for Medical Records
    """
    class Meta:
        model = MedicalRecord
        fields = [
            'id',
            'history',
            'record_type',
            'record_date',
            'diagnosis',
            'treatment',
            'notes',
            'is_confidential',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']