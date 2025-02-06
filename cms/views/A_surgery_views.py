from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.db.models import Q
from datetime import datetime
from ..models.surgery import Surgery, Surgery_Type
from ..models.doctor import Doctor
from ..models.dep import Department, Room
from ..serializers.A_surgery import ASurgerySerializer, ASurgeryTypeSerializer


@api_view(['POST'])
def create_surgery(request):
    """
    Create a new surgery appointment with detailed error handling
    """
    try:
        print("Received surgery data:", request.data)
        serializer = ASurgerySerializer(data=request.data)
        
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(
                {
                    "detail": "Validation error",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Add extra validation for foreign keys
        required_relations = {
            'primary_surgeon': Doctor,
            'surgery_type': Surgery_Type,
            'department': Department,
            'operating_room': Room
        }
        
        for field, model in required_relations.items():
            field_id = request.data.get(field)
            if field_id:
                try:
                    model.objects.get(id=field_id)
                except model.DoesNotExist:
                    return Response(
                        {
                            "detail": f"Invalid {field} ID",
                            "errors": {field: [f"Object with id={field_id} does not exist."]}
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
        surgery = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print("Exception in create_surgery:", str(e))
        return Response(
            {
                "detail": str(e),
                "errors": {"non_field_errors": [str(e)]}
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def get_all_surgeries(request):
    """
    Get all surgeries with optional filters
    """
    surgeries = Surgery.objects.all().order_by('-schedules_start_time')
    serializer = ASurgerySerializer(surgeries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_surgery(request, surgery_id):
    """
    Get details of a specific surgery
    """
    try:
        surgery = Surgery.objects.get(id=surgery_id)
        serializer = ASurgerySerializer(surgery)
        return Response(serializer.data)
    except Surgery.DoesNotExist:
        return Response(
            {"error": "Surgery not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
def update_surgery(request, surgery_id):
    """
    Update a surgery appointment
    """
    try:
        surgery = Surgery.objects.get(id=surgery_id)
        serializer = ASurgerySerializer(surgery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Surgery.DoesNotExist:
        return Response(
            {"error": "Surgery not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
def delete_surgery(request, surgery_id):
    """
    Delete a surgery appointment
    """
    try:
        surgery = Surgery.objects.get(id=surgery_id)
        surgery.delete()
        return Response(
            {"message": "Surgery deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except Surgery.DoesNotExist:
        return Response(
            {"error": "Surgery not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
@api_view(['GET'])
def get_surgeries_by_doctor(request, doctor_id):
    """
    Get all surgeries for a specific doctor
    """
    surgeries = Surgery.objects.filter(primary_surgeon_id=doctor_id).order_by('-schedules_start_time')
    serializer = ASurgerySerializer(surgeries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_surgeries_by_room(request, room_id):
    """
    Get all surgeries scheduled for a specific operating room
    """
    surgeries = Surgery.objects.filter(operating_room_id=room_id).order_by('-schedules_start_time')
    serializer = ASurgerySerializer(surgeries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_surgeries_by_department(request, department_id):
    """
    Get all surgeries in a specific department
    """
    surgeries = Surgery.objects.filter(department_id=department_id).order_by('-schedules_start_time')
    serializer = ASurgerySerializer(surgeries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_upcoming_surgeries(request):
    """
    Get all upcoming surgeries with more detailed status filtering
    """
    from django.utils import timezone
    current_time = timezone.now()
    
    # Get surgeries that are either:
    # 1. Scheduled for the future
    # 2. Currently in progress (Pre-Op, In Surgery, Post-Op, Recovery)
    # 3. Scheduled for today but haven't started yet
    in_progress_statuses = ['Pre-Op', 'In Surgery', 'Post-Op', 'Recovery']
    
    surgeries = Surgery.objects.filter(
        models.Q(schedules_start_time__gt=current_time) |  # Future surgeries
        models.Q(status__in=in_progress_statuses) |        # In-progress surgeries
        models.Q(                                          # Today's scheduled surgeries
            schedules_start_time__date=current_time.date(),
            status='Scheduled'
        )
    ).order_by('schedules_start_time')
    
    serializer = ASurgerySerializer(surgeries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def check_room_availability(request, room_id, start_time, end_time):
    """
    Check if an operating room is available for a given time slot
    """
    try:
        # Convert string times to datetime objects
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        # Check if there are any overlapping surgeries
        conflicts = Surgery.objects.filter(
            operating_room_id=room_id,
            schedules_start_time__lt=end,
            schedules_end_time__gt=start
        ).exists()
        
        if conflicts:
            return Response({
                "available": False,
                "message": "Room is already booked for this time slot"
            })
            
        return Response({
            "available": True,
            "message": "Room is available for this time slot"
        })
        
    except ValueError:
        return Response(
            {"error": "Invalid date format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def get_surgery_statistics(request):
    """
    Get comprehensive surgery statistics including counts by status and department
    """
    from django.utils import timezone
    current_time = timezone.now()
    
    # Total surgeries
    total_surgeries = Surgery.objects.count()
    
    # Get surgeries by status for precise counting
    status_counts = {
        status: Surgery.objects.filter(status=status).count()
        for status, _ in Surgery.STATUS_CHOICES
    }
    
    # Calculate main statistics
    in_progress_statuses = ['Pre-Op', 'In Surgery', 'Post-Op', 'Recovery']
    statistics = {
        "total": total_surgeries,
        "inProgress": sum(status_counts[status] for status in in_progress_statuses),
        "scheduled": Surgery.objects.filter(
            status='Scheduled',
            schedules_start_time__gt=current_time
        ).count(),
        "completed": status_counts['Completed'],
    }
    
    # Department statistics
    department_stats = Surgery.objects.values(
        'department__department_name'
    ).annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    # Surgery type statistics
    type_stats = Surgery.objects.values(
        'surgery_type__type_name'
    ).annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    # Status distribution
    status_stats = Surgery.objects.values(
        'status'
    ).annotate(
        count=models.Count('id')
    ).order_by('status')
    
    # Recent surgeries trend (last 7 days)
    seven_days_ago = current_time - timezone.timedelta(days=7)
    daily_trend = Surgery.objects.filter(
        created_at__gte=seven_days_ago
    ).annotate(
        date=models.functions.TruncDate('created_at')
    ).values('date').annotate(
        count=models.Count('id')
    ).order_by('date')
    
    # Merge all statistics
    statistics.update({
        "byDepartment": list(department_stats),
        "byType": list(type_stats),
        "byStatus": list(status_stats),
        "dailyTrend": list(daily_trend)
    })
    
    return Response(statistics)

@api_view(['GET'])
def get_surgeries_by_status(request, status):
    """
    Get surgeries filtered by status
    """
    if status not in dict(Surgery.STATUS_CHOICES):
        return Response(
            {"error": f"Invalid status. Must be one of {dict(Surgery.STATUS_CHOICES).keys()}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    surgeries = Surgery.objects.filter(status=status).order_by('-schedules_start_time')
    serializer = ASurgerySerializer(surgeries, many=True)
    return Response(serializer.data)