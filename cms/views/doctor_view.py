from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Doctor , DoctorSchedule , User, Room
from ..serializers import DoctorSerializer , DoctorScheduleSerializer
from datetime import datetime


@api_view(['POST'])
def add_doctor(request):
    data = request.data
    serializer = DoctorSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()
        return Response({"message": "Doctor removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_doctor_field(request, doctor_id, field_name):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    field_value = request.data.get(field_name)
    if not field_value:
        return Response({"error": "Field value is required"}, status=status.HTTP_400_BAD_REQUEST)

    setattr(doctor, field_name, field_value)
    doctor.save()
    serializer = DoctorSerializer(doctor)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_doctors_by_department(request, department_id):
    doctors = Doctor.objects.filter(department_id=department_id)
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_available_doctors(request, department_id):
    now = datetime.now()
    current_day = now.weekday()  # 0 = Monday, 6 = Sunday
    current_time = now.time()

    available_doctors = Doctor.objects.filter(
        department_id=department_id,
        schedules__day_of_week=current_day,
        schedules__start_time__lte=current_time,
        schedules__end_time__gte=current_time
    ).distinct()

    serializer = DoctorSerializer(available_doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_doctor_schedule(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    schedules = DoctorSchedule.objects.filter(doctor_id=doctor_id).order_by('start_time')
    serializer = DoctorScheduleSerializer(schedules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_doctor_schedule(request, schedule_id):
    try:
        schedule = DoctorSchedule.objects.get(id=schedule_id)
    except DoctorSchedule.DoesNotExist:
        return Response({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DoctorScheduleSerializer(schedule, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def assign_schedule_to_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['doctor'] = doctor.id
    serializer = DoctorScheduleSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_doctor_by_user_id(request, user_id):
    """
    Retrieve doctor details by user ID.
    """
    try:
        # Find the User instance and then related Doctor instance
        user = User.objects.get(id=user_id)
        doctor = Doctor.objects.get(user=user)

        # Serialize the doctor's details
        doctor_data = {
            "id": doctor.id,
            "user_id": user.id,
            "first_name": doctor.first_name,
            "last_name": doctor.last_name,
            "phone_number": doctor.phone_number,
            "address": doctor.address,
            "license_number": doctor.license_number,
            "department": doctor.department.department_name if doctor.department else None,
            "qualifications": doctor.qualifications,
            "years_of_experience": doctor.years_of_experience,
            "consultation_fee": doctor.consultation_fee,
        }
        return Response(doctor_data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_doctors_by_room(request, room_id):
    """
    Retrieve all doctors assigned to a specific room.
    """
    try:
        # Filter doctors by the room ID
        doctors = Doctor.objects.filter(room_id=room_id)
        if not doctors:
            return Response({"message": "No doctors found for this room."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the list of doctors
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Room.DoesNotExist:
        return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def doctors_list(request):
    """
    Retrieve all rooms
    """
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_doctor_name_by_id(request, doctor_id):
    """
    Retrieve doctor name by ID
    """
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        return Response({
            'name': f"{doctor.first_name} {doctor.last_name}"
        }, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)