from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import jwt
import datetime
from django.conf import settings
from ..models import User


@api_view(['POST'])
def login(request):
    """
    Authenticate user and return JWT token with user details
    """
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # Find user by email
        user = User.objects.get(email=email)
        result = (password == user.password_hash)
        print(result)
        # Check password
        if not result:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Update last login
        user.last_login = timezone.now()
        user.save()

        # Generate JWT token
        token_payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role.id if user.role else None,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }

        # Ensure proper token encoding for Python 3
        token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.id if user.role else None,
                'is_active': user.is_active
            }
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)