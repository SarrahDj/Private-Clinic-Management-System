from rest_framework import serializers
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Appointment, Doctor, Department, Room


class AappointmentSerializer(serializers.ModelSerializer):
    doctor_first_name = serializers.CharField(source='doctor.first_name', read_only=True)
    doctor_last_name = serializers.CharField(source='doctor.last_name', read_only=True)
    department_name = serializers.CharField(source='department_id.department_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def to_internal_value(self, data):
        # Convert emergency_level to integer if it's a string
        if 'emergency_level' in data and isinstance(data['emergency_level'], str):
            try:
                data = data.copy()  # Make a mutable copy
                data['emergency_level'] = int(data['emergency_level'])
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    'emergency_level': 'Emergency level must be a valid integer'
                })

        # Handle foreign keys
        if 'doctor' in data and data['doctor']:
            try:
                Doctor.objects.get(id=data['doctor'])
            except Doctor.DoesNotExist:
                raise serializers.ValidationError({
                    'doctor': f"Doctor with id {data['doctor']} does not exist"
                })

        if 'room' in data and data['room']:
            try:
                Room.objects.get(id=data['room'])
            except Room.DoesNotExist:
                raise serializers.ValidationError({
                    'room': f"Room with id {data['room']} does not exist"
                })

        if 'department_id' in data and data['department_id']:
            try:
                Department.objects.get(id=data['department_id'])
            except Department.DoesNotExist:
                raise serializers.ValidationError({
                    'department_id': f"Department with id {data['department_id']} does not exist"
                })

        return super().to_internal_value(data)

    def validate(self, data):
        # Validate emergency level
        if data.get('is_emergency') and 'emergency_level' not in data:
            raise serializers.ValidationError({
                "emergency_level": "Emergency level is required when is_emergency is True"
            })

        # Ensure end_time is set
        if 'start_time' in data and not data.get('end_time'):
            data['end_time'] = data['start_time'] + timezone.timedelta(hours=1)

        # Ensure notes field is preserved
        if 'notes' in self.initial_data:
            data['notes'] = self.initial_data['notes']

        return data

    def create(self, validated_data):
        # Ensure all required fields are present
        for field in ['doctor', 'room', 'department_id']:
            if field in validated_data and validated_data[field]:
                model_class = {
                    'doctor': Doctor,
                    'room': Room,
                    'department_id': Department
                }[field]
                try:
                    if isinstance(validated_data[field], (str, int)):
                        validated_data[field] = model_class.objects.get(id=validated_data[field])
                except model_class.DoesNotExist:
                    raise serializers.ValidationError(f"{field} not found")

        # Create the appointment
        appointment = Appointment.objects.create(**validated_data)
        return appointment