from rest_framework import serializers
from ..models import Doctor, DoctorSchedule

class DoctorSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='user.role.role_name', read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'


