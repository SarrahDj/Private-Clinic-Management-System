import jwt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def validate_token(token):
    """
    Validate JWT token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(view_func):
    """
    Decorator to require valid JWT token for views
    """
    def wrapper(request, *args, **kwargs):
        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return Response({
                'error': 'Authorization token is required'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Remove 'Bearer ' prefix if present
            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
            payload = validate_token(token)

            if not payload:
                return Response({
                    'error': 'Invalid or expired token'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Attach user info to request for use in view
            request.user_id = payload.get('user_id')
            request.user_role = payload.get('role')

        except Exception as e:
            return Response({
                'error': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kwargs)
    return wrapper