from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Appointment, Doctor, Department, Room
from ..serializers import AppointmentSerializer

# List all appointments or create a new appointment
@api_view(['GET', 'POST'])
def appointment_list_create(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        allowed_fields = ['patient_full_name', 'patient_address', 'patient_phone_number', 'start_time', 'is_emergency', 'department_id']
        data = {field: request.data.get(field) for field in allowed_fields}

        data['status'] = 'Scheduled'  # Default status
        data['doctor'] = None
        data['room'] = None
        data['notes'] = None
        data['emergency_level'] = None
        data['created_by'] = None
        data['updated_by'] = None
        data['end_time'] = None

        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['²', 'PUT', 'DELETE'])
def appointment_detail(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    # Handle GET request
    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    # Handle PUT request (partial updates allowed)
    if request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE request
    if request.method == 'DELETE':
        appointment.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Cancel an appointment
@api_view(['POST'])
def cancel_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    appointment.status = "Cancelled"
    appointment.save()
    return Response({"message": "Appointment cancelled successfully."}, status=status.HTTP_200_OK)


# List scheduled appointments of a specific doctor (by doctor id)
@api_view(['GET'])
def scheduled_appointments_by_doctor(request, doctor_id):
    appointments = Appointment.objects.filter(doctor_id=doctor_id).order_by('start_time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# List scheduled appointments of a specific patient (filter by email address)
@api_view(['GET'])
def scheduled_appointments_by_patient_email(request, email):
    appointments = Appointment.objects.filter(patient_address=email).order_by('start_time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Modify only date and time (start_time and end_time)
@api_view(['PUT'])
def modify_appointment_datetime(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')

    if start_time:
        appointment.start_time = start_time
    if end_time:
        appointment.end_time = end_time

    appointment.save()

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Display specific fields: full name, date, time, room, and notes, for doctor appointment interface
@api_view(['GET'])
def appointment_summary(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'patient_full_name': appointment.patient_full_name,
        'date': appointment.start_time.date(),
        'time': appointment.start_time.time(),
        'room': appointment.room.room_number if appointment.room else None,
        'notes': appointment.notes
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_doctor_name_by_appointment_id(request, appointment_id):
    """
    Retrieve the doctor's name based on the appointment ID.
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        doctor = appointment.doctor

        if doctor:
            return Response({"doctor_name": f"{doctor.first_name} {doctor.last_name}"}, status=status.HTTP_200_OK)
        else:
            return Response({"doctor_name": "No doctor assigned to this appointment."},
                            status=status.HTTP_404_NOT_FOUND)

    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)


# views.py
from rest_framework import generics

class PatientAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        return Appointment.objects.filter(created_by__email=email)


@api_view(['GET', 'POST'])
def appointment_list_create_cms(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("Received data:", request.data)
        allowed_fields = ['patient_full_name', 'patient_address', 'patient_phone_number', 'start_time','end_time',  'department',
                           'doctor','room','is_emergency','emergency_level','status','notes']
        data = {field: request.data.get(field) for field in allowed_fields}
        serializer = AppointmentSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            # Set created/updated by to current user if authenticated
            if request.user.is_authenticated:
                serializer.validated_data['created_by'] = request.user
                serializer.validated_data['updated_by'] = request.user


            if 'doctor' in request.data:
                try:
                    # Try to find doctor by ID first
                    doctor = Doctor.objects.get(id=request.data['doctor'])
                    serializer.validated_data['doctor'] = doctor
                except Doctor.DoesNotExist:
                    return Response({"error": "Doctor not found"}, status=status.HTTP_400_BAD_REQUEST)

            if 'department' in request.data:
                try:
                    # Try to find department by ID first
                    department = Department.objects.get(id=request.data['department'])
                    serializer.validated_data['department_name'] = department.department_name
                except Department.DoesNotExist:
                    return Response({"error": "Invalid department."}, status=status.HTTP_400_BAD_REQUEST)

            if 'room' in request.data:
                try:
                    room = Room.objects.get(id=request.data['room'])
                    serializer.validated_data['room'] = room
                except Room.DoesNotExist:
                    return Response({"error": "Room with the provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def appointment_detail_cms(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer =AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            # Map department if provided by name
            if 'department' in request.data:
                try:
                    department = Department.objects.get(department_name=request.data['department'])
                    serializer.validated_data['department'] = department
                except Department.DoesNotExist:
                    return Response({"error": "Invalid department name"}, status=status.HTTP_400_BAD_REQUEST)

            # Map doctor if provided by name
            if 'doctor' in request.data:
                try:
                    doctor = Doctor.objects.get(name=request.data['doctor'])
                    serializer.validated_data['doctor'] = doctor
                except Doctor.DoesNotExist:
                    return Response({"error": "Doctor with the provided name does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Map room if provided by room number
            if 'room' in request.data:
                try:
                    room = Room.objects.get(room_number=request.data['room'])
                    serializer.validated_data['room'] = room
                except Room.DoesNotExist:
                    return Response({"error": "Room with the provided number does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appointment.delete()
        return Response(
            {"message": "Appointment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['PUT'])
def update_appointment(request, pk):
    """
    Updates an existing appointment with the provided data.
    Handles mapping of related fields like doctor, department, and room.
    """
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Extract the data from the request
    data = request.data

    # Map doctor if provided
    if 'doctor' in data:
        try:
            doctor = Doctor.objects.get(id=data['doctor'])
            data['doctor'] = doctor.id  # Replace with doctor ID
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Map department if provided
    if 'department' in data:
        try:
            department = Department.objects.get(id=data['department'])
            data['department'] = department.id  # Replace with department ID
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Map room if provided
    if 'room' in data:
        try:
            room = Room.objects.get(id=data['room'])
            data['room'] = room.id  # Replace with room ID
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Update the appointment
    serializer = AppointmentSerializer(appointment, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)