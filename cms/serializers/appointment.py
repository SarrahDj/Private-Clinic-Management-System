from rest_framework import serializers
from ..models import Appointment,  User

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_first_name = serializers.CharField(source='doctor.first_name', read_only=True)
    doctor_last_name = serializers.CharField(source='doctor.last_name', read_only=True)
    department_name = serializers.CharField(source='department_id.department_name', read_only=True)
    doctor_image = serializers.SerializerMethodField( read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        extra_fields = ['doctor_first_name', 'doctor_last_name', 'department_name', 'doctor_image']

    def get_doctor_image(self, obj):
        """
        Retrieve the profile image of the user associated with the doctor.
        Handles cases where user or image may not exist.
        """
        try:
            user = User.objects.get(
                doctor_profiles__first_name=obj.doctor.first_name,
                doctor_profiles__last_name=obj.doctor.last_name,
                doctor_profiles__address=obj.doctor.address
            )
            return user.profile_image if user.profile_image else "No image available"
        except User.DoesNotExist:
            return "No image available"
        except AttributeError:
            # Handles cases where `doctor` or its attributes are null
            return "No image available"

    def create(self, validated_data):
        # Handle nested or extra fields if required
        department = validated_data.pop('department', None)

        # Map 'department' to the appropriate field in the model
        if department:
            validated_data['department_id'] = department

        # Create and return the Appointment instance
        return super().create(validated_data)
