from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Patient ,  User , Role
from ..serializers import PatientSerializer, UserSerializer


@api_view(['POST'])
def add_patient(request):
    """
    Add a new patient with automatic user creation if user doesn't exist.
    """
    try:
        # Extract email from the patient data
        email = request.data.get('email')

        if not email:
            return Response(
                {"error": "Email is required to create a patient profile"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to find the user by email
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user with default parameters
            try:
                # Get the default role (assuming you have a default patient role)
                default_role = Role.objects.get(
                    role_name='Patient')  # You might need to adjust this based on your role setup

                # Create user data
                user_data = {
                    'email': email,
                    'username': email.split('@')[0],  # Use part before @ as username
                    'password_hash': '12345678',  # Default password
                    'role': default_role.id,
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

        # Create a copy of request data and add the user
        patient_data = request.data.copy()
        patient_data['user'] = user.id

        # Create the patient serializer with the updated data
        serializer = PatientSerializer(data=patient_data)

        if serializer.is_valid():
            # Save the patient with the associated user
            patient = serializer.save()
            return Response({
                "message": "Patient created successfully",
                "user_created": user is not None,
                "patient_data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_patient_by_user_id(request, user_id):
    """
    Retrieve patient details by user ID.
    """
    try:
        # Find the User instance and then the related Patient instance
        user = User.objects.get(id=user_id)
        patient = Patient.objects.get(user=user)  # Assuming MedicalRecord has a ForeignKey to User

        # Serialize the patient's details
        patient_data = {
            "id": patient.id,
            "user_id": user.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": patient.date_of_birth,
            "gender": patient.gender,
            "blood_type": patient.blood_type,
            "address_line": patient.address_line,
            "city": patient.city,
            "state": patient.state,
            "postal_code": patient.postal_code,
            "country": patient.country,
            "phone_primary": patient.phone_primary,
            "email": patient.email,
            "last_visit_date": patient.last_visit_date,
            "patient_type": patient.patient_type,
            "status": patient.status,
        }
        return Response({"patient_data": patient_data}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Patient.DoesNotExist:
        return Response({"error": "Patient profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_patient(request, patient_id):
    """
    Remove a patient by ID.
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        patient.delete()
        return Response({"message": "Patient removed successfully."}, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_patient(request, patient_id):
    """
    Update patient details.
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        serializer = PatientSerializer(patient, data=request.data, partial=True)  # `partial=True` allows updating specific fields
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient updated successfully.", "patient_data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def show_all_patients(request):
    """
    Display all patients.
    """
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response({"patients": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def show_patient(request, patient_id):
    """
    Display details of a single patient.
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        serializer = PatientSerializer(patient)
        return Response({"patient_data": serializer.data}, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

