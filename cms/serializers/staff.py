from rest_framework import serializers
from ..models import Staff

class StaffSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'  # Include all fields


