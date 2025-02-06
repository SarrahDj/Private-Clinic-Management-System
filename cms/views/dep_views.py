from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Department, Room
from ..serializers import DepartmentSerializer, RoomSerializer

# Add a Department
@api_view(['POST'])
def add_department(request):
    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all Departments
@api_view(['GET'])
def get_all_departments(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

# Delete a Department
@api_view(['DELETE'])
def delete_department(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    department.delete()
    return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Add a Room
@api_view(['POST'])
def add_room(request):
    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a Room
@api_view(['DELETE'])
def delete_room(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    room.delete()
    return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Update Room Capacity
@api_view(['PUT'])
def update_room_capacity(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    new_capacity = request.data.get('capacity')
    if new_capacity:
        room.capacity = new_capacity
        room.save()
        return Response({"message": "Room capacity updated successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Capacity not provided"}, status=status.HTTP_400_BAD_REQUEST)

# Update Room Availability
@api_view(['PUT'])
def update_room_availability(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    new_availability = request.data.get('is_available')
    if new_availability is not None:
        room.is_available = new_availability
        room.save()
        return Response({"message": "Room availability updated successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Availability not provided"}, status=status.HTTP_400_BAD_REQUEST)

# Retrieve available rooms in a specific department
@api_view(['GET'])
def available_rooms_in_department(request, department_id):
    available_rooms = Room.objects.filter(department_id=department_id, is_available=True)
    serializer = RoomSerializer(available_rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def departments_list(request):
    """
    Retrieve all departments
    """
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def rooms_list(request):
    """
    Retrieve all rooms
    """
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_department_name_by_id(request, department_id):
    """
    Retrieve department name by ID
    """
    try:
        department = Department.objects.get(id=department_id)
        return Response({
            'name': department.department_name
        }, status=status.HTTP_200_OK)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_room_number_by_id(request, room_id):
    """
    Retrieve room number by ID
    """
    try:
        room = Room.objects.get(id=room_id)
        return Response({
            'number': room.room_number
        }, status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)