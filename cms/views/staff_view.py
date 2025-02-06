# staff_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ..models import User, Staff, Role, Doctor, Department
from ..serializers import UserSerializer, StaffSerializer, DoctorSerializer


@api_view(['POST'])
def create_staff_member(request):
    """
    Create a staff member with role-based assignment and automatic user creation if needed
    """
    try:
        with transaction.atomic():
            # Extract and validate basic data
            email = request.data.get('email')
            role_name = request.data.get('role')

            if not email or not role_name:
                return Response(
                    {"error": "Email and role are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get and validate role first
            try:
                role = Role.objects.get(role_name=role_name)
            except Role.DoesNotExist:
                return Response(
                    {"error": "Invalid role specified"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find or create user
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create new user with default parameters
                try:
                    user_data = {
                        'email': email,
                        'username': email.split('@')[0],  # Use part before @ as username
                        'password_hash': '12345678',  # Default password
                        'role': role.id,
                        'is_active': True
                    }

                    # Create new user
                    user_serializer = UserSerializer(data=user_data)
                    if user_serializer.is_valid():
                        user = user_serializer.save()
                    else:
                        return Response(
                            {"error": "Failed to create user", "details": user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except Exception as e:
                    return Response(
                        {"error": f"Error creating new user: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Validate department if provided
            department_id = request.data.get('department')
            department = None
            if department_id:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    return Response(
                        {"error": "Invalid department"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Prepare common staff data
            staff_data = {
                'user': user.id,
                'role': role.id,
                'email': user.email,
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'phone_number': request.data.get('phone_number'),
                'address': request.data.get('address'),
                'license_number': request.data.get('license_number'),
                'qualifications': request.data.get('qualifications'),
                'years_of_experience': request.data.get('years_of_experience'),
                'department': department.id if department else None,
                'shift_preference': request.data.get('shift_preference'),
                'start_date': request.data.get('start_date')
            }

            # Update user's role
            user.role = role
            user.save()

            # Handle doctor-specific creation
            if role.role_name.lower() == 'doctor':
                # Validate doctor-specific fields
                consultation_fee = request.data.get('consultation_fee')
                if not consultation_fee:
                    return Response(
                        {"error": "Consultation fee is required for doctors"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                doctor_data = {
                    **staff_data,
                    'consultation_fee': consultation_fee
                }

                # Check if doctor already exists
                existing_doctor = Doctor.objects.filter(user=user).first()
                if existing_doctor:
                    serializer = DoctorSerializer(existing_doctor, data=doctor_data)
                else:
                    serializer = DoctorSerializer(data=doctor_data)

            else:
                # Handle regular staff creation
                existing_staff = Staff.objects.filter(user=user).first()
                if existing_staff:
                    serializer = StaffSerializer(existing_staff, data=staff_data)
                else:
                    serializer = StaffSerializer(data=staff_data)

            if serializer.is_valid():
                staff_member = serializer.save()
                response_data = {
                    "message": f"{'Doctor' if role.role_name.lower() == 'doctor' else 'Staff member'} created successfully",
                    "user_created": user is not None,
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_staff_by_user_id(request, user_id):
    """
    Retrieve staff details based on user ID and role
    """
    try:
        user = User.objects.get(id=user_id)
        role = user.role  # Assuming User model has a role field

        if role.role_name.lower() == 'doctor':
            staff = Doctor.objects.get(user=user)
            serializer = DoctorSerializer(staff)
        else:
            staff = Staff.objects.get(user=user)
            serializer = StaffSerializer(staff)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except (User.DoesNotExist, Staff.DoesNotExist, Doctor.DoesNotExist) as e:
        return Response(
            {"error": "Staff member not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
def delete_staff_member(request, staff_id , role_name):
    """
    Delete a staff member based on user ID and role
    """
    try:

          print(role_name)# Assuming User model has a role field
          if role_name.lower() == 'doctor':
            staff = Doctor.objects.get(id=staff_id)
            staff.delete()
            return Response(
                {"message": "Doctor removed successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
          else:
        # Delete regular staff member
            staff = Staff.objects.get(id= staff_id)
            staff.delete()
            return Response(
                {"message": "Staff member removed successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

    except (User.DoesNotExist, Staff.DoesNotExist, Doctor.DoesNotExist) as e:
        return Response(
            {"error": "Staff member not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
def update_staff_member(request, user_id):
    """
    Update staff member details based on user ID and role
    """
    try:
        user = User.objects.get(id=user_id)
        role = user.role

        # Collect updatable fields
        update_data = {}
        updatable_fields = [
            'first_name', 'last_name', 'phone_number', 'address',
            'qualifications', 'years_of_experience', 'shift_preference',
            'start_date', 'department', 'license_number'
        ]

        for field in updatable_fields:
            if field in request.data:
                update_data[field] = request.data.get(field)

        if role.role_name.lower() == 'doctor':
            # Update doctor-specific details
            doctor = Doctor.objects.get(user=user)

            # Additional doctor-specific fields
            doctor_specific_fields = ['consultation_fee', 'specialty', 'is_surgeon']
            for field in doctor_specific_fields:
                if field in request.data:
                    update_data[field] = request.data.get(field)

            # Handle department separately
            if 'department' in update_data:
                try:
                    department = Department.objects.get(id=update_data['department'])
                    update_data['department'] = department
                except Department.DoesNotExist:
                    return Response(
                        {"error": "Invalid department"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Update doctor fields
            for key, value in update_data.items():
                setattr(doctor, key, value)
            doctor.save()

            serializer = DoctorSerializer(doctor)
            model_name = "Doctor"

        else:
            # Update regular staff member
            staff = Staff.objects.get(user=user)

            # Handle department separately
            if 'department' in update_data:
                try:
                    department = Department.objects.get(id=update_data['department'])
                    update_data['department'] = department
                except Department.DoesNotExist:
                    return Response(
                        {"error": "Invalid department"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Update staff fields
            for key, value in update_data.items():
                setattr(staff, key, value)
            staff.save()

            serializer = StaffSerializer(staff)
            model_name = "Staff"

        return Response(
            {
                "message": f"{model_name} updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    except (User.DoesNotExist, Staff.DoesNotExist, Doctor.DoesNotExist) as e:
        return Response(
            {"error": "Staff member not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def list_all_staff(request):
    """
    Retrieve a list of all staff members (both doctors and regular staff)
    """
    # Retrieve doctors
    doctors = Doctor.objects.all()
    doctor_serializer = DoctorSerializer(doctors, many=True)

    # Retrieve regular staff
    staff = Staff.objects.all()
    staff_serializer = StaffSerializer(staff, many=True)

    return Response({
        "doctors": doctor_serializer.data,
        "staff": staff_serializer.data
    }, status=status.HTTP_200_OK)

