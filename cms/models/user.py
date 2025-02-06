from django.db import models
from .role import Role
from django.contrib.auth.hashers import check_password

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    profile_image = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        """
        Check if the provided password matches the stored password.
        """
        return check_password(raw_password, self.password_hash)
