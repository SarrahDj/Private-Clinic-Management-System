from rest_framework import serializers
from ..models.surgery import Surgery, Surgery_Type

class ASurgeryTypeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    
    class Meta:
        model = Surgery_Type
        fields = ['id', 'type_name', 'description', 'department', 'department_name', 'typical_duration_min', 
                 'preparation_instructions', 'recovery_instructions']

class ASurgerySerializer(serializers.ModelSerializer):
    # Doctor related fields
    primary_surgeon_first_name = serializers.CharField(source='primary_surgeon.first_name', read_only=True)
    primary_surgeon_last_name = serializers.CharField(source='primary_surgeon.last_name', read_only=True)
    primary_surgeon_full_name = serializers.SerializerMethodField()
    
    # Surgery type related field
    surgery_type_name = serializers.CharField(source='surgery_type.type_name', read_only=True)
    
    # Room related fields
    operating_room_number = serializers.IntegerField(source='operating_room.room_number', read_only=True)
    operating_room_type = serializers.CharField(source='operating_room.type', read_only=True)
    operating_room_available = serializers.BooleanField(source='operating_room.is_available', read_only=True)
    
    # Department related fields
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    
    status = serializers.CharField(required=True)
    
    def get_primary_surgeon_full_name(self, obj):
        if obj.primary_surgeon:
            return f"Dr. {obj.primary_surgeon.first_name} {obj.primary_surgeon.last_name}"
        return None

    class Meta:
        model = Surgery
        fields = [
            'id', 
            'patient_full_name',

            'primary_surgeon',
            'primary_surgeon_first_name',
            'primary_surgeon_last_name',
            'primary_surgeon_full_name',

            'surgery_type',
            'surgery_type_name',
            
            'department',
            'department_name',
            
            'operating_room',
            'operating_room_number',
            'operating_room_type',
            'operating_room_available',

            'schedules_start_time',
            'schedules_end_time',
            'actual_start_time',
            'actual_end_time',
            
            'pre_op_notes',
            'post_op_notes',
            'complications',
            
            'created_at',
            'updated_at',
            
            'status' 
        ]
        
    def validate(self, data):
        # First validate required fields
        required_fields = [
            'patient_full_name',
            'primary_surgeon',
            'surgery_type',
            'department',
            'operating_room',
            'schedules_start_time',
            'schedules_end_time',
            'status'
        ]
        
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")

        # Existing validations...
        if ('schedules_end_time' in data and 'schedules_start_time' in data and 
            data['schedules_end_time'] <= data['schedules_start_time']):
            raise serializers.ValidationError({
                "schedules_end_time": "Scheduled end time must be after scheduled start time"
            })
            
        if ('actual_end_time' in data and data['actual_end_time'] is not None and
            'actual_start_time' in data and data['actual_start_time'] is not None and
            data['actual_end_time'] <= data['actual_start_time']):
            raise serializers.ValidationError({
                "actual_end_time": "Actual end time must be after actual start time"
            })

        # Validate operating room availability
        if 'operating_room' in data and not data['operating_room'].is_available:
            raise serializers.ValidationError({
                "operating_room": "Selected operating room is not available"
            })

        # Validate doctor's department matches surgery department
        if ('primary_surgeon' in data and 'department' in data and 
            data['primary_surgeon'].department != data['department']):
            raise serializers.ValidationError({
                "primary_surgeon": "Primary surgeon must be from the same department"
            })

        return data

    def validate_status(self, value):
        valid_statuses = ['Scheduled', 'Pre-Op', 'In Surgery', 'Post-Op', 'Recovery', 'Completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value

    def create(self, validated_data):
        # Add any default values for non-required fields
        validated_data.setdefault('pre_op_notes', '')
        validated_data.setdefault('post_op_notes', '')
        validated_data.setdefault('complications', '')
        validated_data.setdefault('actual_start_time', None)
        validated_data.setdefault('actual_end_time', None)
        
        return super().create(validated_data)