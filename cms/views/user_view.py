from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..models import User
from ..serializers import UserSerializer

@api_view(['POST'])
def create_user(request):
    """
    Create a new user.
    """
    data = request.data
    passw = data.get('password')
    print(data)

    serializer = UserSerializer(data=data)
    print (serializer)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_user(request, user_id):
    """
    Remove a user by ID.
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'success': f'User with ID {user_id} has been removed.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_user_profile(request, user_id):
    """
    Update user profile with comprehensive validation.
    """
    try:
        user = User.objects.get(id=user_id)
        data = request.data

        # Validate and update specific fields
        allowed_fields = ['username', 'email', 'profile_image']

        for field in allowed_fields:
            if field in data:
                if field == 'email':
                    # Email validation
                    import re
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", data[field]):
                        return Response(
                            {"error": "Invalid email format"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                setattr(user, field, data[field])

        user.save()

        # Return updated user details
        return Response({
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_image": user.profile_image
            }
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_field(request, user_id):
    """
    Retrieve specific fields of a user.
    """
    try:
        user = User.objects.get(id=user_id)
        fields = request.query_params.getlist('fields')  # List of fields to retrieve

        if not fields:
            return Response({"error": "No fields specified."}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {field: getattr(user, field, "Field not found") for field in fields}
        return Response({"user_data": user_data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_users(request):
    """
    Display all users.
    """
    try:
        users = User.objects.all()
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.role_name if user.role else None,
                "is_active": user.is_active,
                "last_login": user.last_login,
                "created_at": user.created_at,
            }
            for user in users
        ]
        return Response({"users": users_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def change_password(request):
    """
    Change user password with current password verification.
    """
    user_id = request.data.get('user_id')  # Match the frontend payload
    current_password = request.data.get('current_password')  # Match the frontend payload
    new_password = request.data.get('new_password')  # Match the frontend payload

    try:
        user = User.objects.get(id=user_id)

        # Add current password verification
        if not user.check_password(current_password):
            return Response(
                {"message": "Current password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Password complexity checks
        if len(new_password) < 8:
            return Response(
                {"message": "Password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional: Add more password complexity checks
        import re
        if not re.search(r'[A-Z]', new_password):
            return Response(
                {"message": "Password must contain at least one uppercase letter"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.search(r'[a-z]', new_password):
            return Response(
                {"message": "Password must contain at least one lowercase letter"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.search(r'\d', new_password):
            return Response(
                {"message": "Password must contain at least one number"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            return Response(
                {"message": "Password must contain at least one special character"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set and hash new password
        user.password_hash = make_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def get_user_details(request, user_id):
    """
    Retrieve and display user details by ID.
    """
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.id if user.role else None,
            "profile_image": user.profile_image,
            "is_active": user.is_active,
            "last_login": user.last_login,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        return Response(user_data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)