from rest_framework import serializers
from ..models import Department, Room

# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'description']

# Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'department', 'capacity', 'room_number', 'type', 'is_available']
