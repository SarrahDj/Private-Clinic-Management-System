from rest_framework import serializers
from ..models import User, Role

class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', "password_hash", 'profile_image', 'is_active']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

    def validate_email(self, value):
        # Email unique validation
        if User.objects.exclude(pk=self.instance.pk if self.instance else None).filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value