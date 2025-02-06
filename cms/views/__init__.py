from .appointment_views import cancel_appointment, appointment_list_create ,appointment_detail, scheduled_appointments_by_doctor, scheduled_appointments_by_patient_email , get_doctor_name_by_appointment_id
from .dep_views import add_department, delete_department, get_all_departments , add_room , delete_room, available_rooms_in_department, update_room_availability, update_room_capacity
from .doctor_view import add_doctor, remove_doctor, update_doctor_field, get_doctor_schedule, get_available_doctors, get_doctors_by_department,update_doctor_schedule, assign_schedule_to_doctor, get_doctor_by_user_id
from .role_view import add_role, delete_role, update_role
from .prescription_view import create_prescription , retrieve_prescription ,update_prescription, retrieve_prescription_by_consultation , retrieve_all_prescriptions
from .category_view import category_list, category_create, category_detail
from .inventory_views import inventory_create, inventory_detail, inventory_list, update_stock
from .supplier_view import supplier_create, supplier_list, supplier_detail
from .log_views import log_list
from .A_surgery_type_views import get_surgery_types_by_department, create_surgery_type, get_all_surgery_types
from .A_surgery_views import get_surgeries_by_department, get_surgeries_by_doctor, get_surgeries_by_room, get_surgery, get_surgery_statistics, create_surgery, delete_surgery, update_surgery, get_all_surgeries, get_upcoming_surgeries
