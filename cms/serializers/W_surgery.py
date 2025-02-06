from rest_framework import serializers
from ..models.surgery import Surgery, Surgery_Type
from ..models.doctor import Doctor 
from ..serializers.dep import DepartmentSerializer
import random 

class WSurgeryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surgery_Type
        fields = ['id', 'type_name', 'department', 'typical_duration_min', 'description']

class WSurgerySerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='surgery_type.type_name', read_only=True)
    team_count = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Surgery
        fields = [
            'id', 
            'patient_full_name',
            'type_name',
            'surgery_type',
            'primary_surgeon',
            'doctor_name',
            'department',  # Add department to fields
            'schedules_start_time',
            'schedules_end_time',
            'actual_start_time',
            'actual_end_time',
            'operating_room',
            'team_count',
            'pre_op_notes',
            'post_op_notes',
            'complications',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['actual_start_time', 'actual_end_time', 'created_at', 'updated_at']
        extra_kwargs = {
            'primary_surgeon': {'required': True},  # Make primary_surgeon required
            'surgery_type': {'required': True},  # Make surgery_type required
            'operating_room': {'required': False},  # Make operating_room optional
            'post_op_notes': {'required': False},  # Make post_op_notes optional
            'complications': {'required': False},  # Make complications optional
        }

    def get_team_count(self, obj):
        return random.randint(4, 8)
    
    def get_doctor_name(self, obj):
        if obj.primary_surgeon:
            return f"{obj.primary_surgeon.first_name} {obj.primary_surgeon.last_name}"
        return None

    def create(self, validated_data):
        # Set default values for optional fields
        validated_data.setdefault('operating_room', None)
        validated_data.setdefault('post_op_notes', None)
        validated_data.setdefault('complications', None)
        validated_data.setdefault('actual_start_time', None)
        validated_data.setdefault('actual_end_time', None)
        validated_data.setdefault('status', 'Scheduled')
        
        if 'department' not in validated_data and 'surgery_type' in validated_data:
            validated_data['department'] = validated_data['surgery_type'].department
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle completion-specific updates
        if validated_data.get('status') == 'Completed':
            instance.actual_end_time = validated_data.get('actual_end_time', None)
            instance.post_op_notes = validated_data.get('post_op_notes', None)
            instance.complications = validated_data.get('complications', None)
        
        return super().update(instance, validated_data)

    def validate(self, data):
        """
        Custom validation for the surgery data.
        """
        # Validate that end time is after start time
        if (data.get('schedules_end_time') and 
            data.get('schedules_start_time') and 
            data['schedules_end_time'] <= data['schedules_start_time']):
            raise serializers.ValidationError({
                "schedules_end_time": "End time must be after start time"
            })
        
        # Ensure primary_surgeon exists
        if 'primary_surgeon' in data:
            try:
                doctor = Doctor.objects.get(id=data['primary_surgeon'].id)
            except Doctor.DoesNotExist:
                raise serializers.ValidationError({
                    "primary_surgeon": "Invalid doctor ID provided"
                })
        
        return data
    
class SurgeryTypeDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Surgery_Type
        fields = [
            'id',
            'type_name',
            'department',
            'description',
            'typical_duration_min',
            'preparation_instructions',
            'recovery_instructions'
        ]
