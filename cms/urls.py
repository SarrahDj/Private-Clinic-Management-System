from django.urls import path
from .views import W_surgery_views, dep_views , doctor_view, appointment_views, role_view, prescription_view
from .views import user_view
from .views import auth_view
from .views import patient_view
from .views import records_view
from .views import staff_view
from .views import category_view
from .views import inventory_views
from .views import log_views
from .views import supplier_view
from .views import A_surgery_views
from .views import A_surgery_type_views
from .views import consultation_view , billing_view
from .views import A_appointment_views



urlpatterns = [
    path('appointments/', appointment_views.appointment_list_create, name='appointment-list-create'),
    path('appointments/cms/', A_appointment_views.appointment_list, name='appointment-list-create-cms'),
    path('appointments/cms/<int:pk>/', A_appointment_views.appointment_detail, name='appointment-detail'),
    path('appointments/<int:pk>/cancel/', appointment_views.cancel_appointment, name='appointment-cancel'),
    path('appointments/doctor/<int:doctor_id>/', appointment_views.scheduled_appointments_by_doctor, name='appointments-by-doctor'),
    path('appointments/patient/<str:email>/', appointment_views.scheduled_appointments_by_patient_email,
         name='appointments-by-patient-email'),
    path('appointments/<int:appointment_id>/doctor/', appointment_views.get_doctor_name_by_appointment_id,
         name='get_doctor_name_by_appointment_id'),
    
    #auth view
    path('login/', auth_view.login, name='login'),

    path('departments/', dep_views.add_department, name='add-department'),
    path('departments/list/', dep_views.departments_list, name='get-list-departments'),
    path('departments/all/', dep_views.get_all_departments, name='get-all-departments'),
    path('departments/delete/<int:pk>/', dep_views.delete_department, name='delete-department'),
    path('departments/<int:department_id>/', dep_views.get_department_name_by_id, name='get_department_name_by_id'),


    path('rooms/', dep_views.add_room, name='add-room'),
    path('rooms/delete/<int:pk>/', dep_views.delete_room, name='delete-room'),
    path('rooms/update-capacity/<int:pk>/', dep_views.update_room_capacity, name='update-room-capacity'),
    path('rooms/update-availability/<int:pk>/', dep_views.update_room_availability, name='update-room-availability'),
    path('rooms/available/<int:department_id>/', dep_views.available_rooms_in_department, name='available-rooms-in-department'),
    path('rooms/list/', dep_views.rooms_list, name='get-list-rooms'),
    path('rooms/<int:room_id>/', dep_views.get_room_number_by_id, name='get_room_number_by_id'),

    # Doctor routes
    path('doctor/', doctor_view.add_doctor, name='add-doctor'),
    path('doctor/<int:doctor_id>/', doctor_view.remove_doctor, name='remove-doctor'),
    path('doctor/<int:doctor_id>/<str:field_name>/', doctor_view.update_doctor_field, name='update-doctor-field'),
    path('doctors/department/<int:department_id>/', doctor_view.get_doctors_by_department, name='get-doctors-by-department'),
    path('doctors/available/<int:department_id>/', doctor_view.get_available_doctors, name='get-available-doctors'),
    path('doctors/room/<int:room_id>/', doctor_view.get_doctors_by_room, name='get-doctors-by-room'),
    path('doctors/list/', doctor_view.doctors_list, name='get-list-doctors'),
    path('doctor/<int:doctor_id>/', doctor_view.get_doctor_name_by_id, name='get_doctor_name_by_id'),

    # Doctor schedule routes
    path('doctor/<int:doctor_id>/schedule/', doctor_view.get_doctor_schedule, name='get-doctor-schedule'),
    path('doctor/schedule/<int:schedule_id>/', doctor_view.update_doctor_schedule, name='update-doctor-schedule'),
    path('doctor/<int:doctor_id>/schedule/assign/', doctor_view.assign_schedule_to_doctor, name='assign-schedule-to-doctor'),
    path('doctor/user/<int:user_id>/', doctor_view.get_doctor_by_user_id, name='get_doctor_by_user_id'),
    path('doctors/room/<int:room_id>/', doctor_view.get_doctors_by_room, name='get-doctors-by-room'),

    # Role routes
    path('role/', role_view.add_role, name='add-role'),
    path('role/<int:role_id>/', role_view.delete_role, name='delete-role'),
    path('role/<int:role_id>/update', role_view.update_role, name='update-role'),
    path('roles/', role_view.list_roles, name='list-roles'),

     # prescription views
    path('prescriptions/', prescription_view.create_prescription, name='create-prescription'),
    path('prescriptions/<int:pk>/', prescription_view.retrieve_prescription, name='retrieve-prescription'),
    path('prescriptions/<int:pk>/update/', prescription_view.update_prescription, name='update-prescription'),
    path('prescriptions/consultation/<int:consultation_id>/', prescription_view.retrieve_prescription_by_consultation, name='retrieve-prescriptions-by-consultation'),
    path('prescriptions/all/', prescription_view.retrieve_all_prescriptions, name='retrieve_all_prescriptions'),
path('prescriptions/<int:pk>/delete/', prescription_view.delete_prescription, name='prescription-delete'),
    # for users view
    path('users/create/', user_view.create_user, name='create_user'),
    path('users/', user_view.get_all_users, name='get_all_users'),
    path('users/remove/<int:user_id>/', user_view.remove_user, name='remove_user'),
    path('users/<int:user_id>/update/', user_view.update_user_profile, name='update_user_profile'),
    path('users/<int:user_id>/fields/', user_view.get_user_field, name='get_user_field'),
    path('users/<int:user_id>/details/', user_view.get_user_details, name='get_user_details'),
    path('users/change-password/', user_view.change_password, name='change_password'),



    path('patient/user/<int:user_id>/', patient_view.get_patient_by_user_id, name='get_patient_by_user_id'),
    path('patients/add/', patient_view.add_patient, name='add_patient'),
    path('patients/<int:patient_id>/remove/', patient_view.remove_patient, name='remove_patient'),
    path('patients/<int:patient_id>/update/', patient_view.update_patient, name='update_patient'),
    path('patients/', patient_view.show_all_patients, name='show_all_patients'),
    path('patients/<int:patient_id>/', patient_view.show_patient, name='show_patient'),

    # Get medical records for a patient
    path('patients/<int:patient_id>/medical-records/',
         records_view.get_patient_medical_records,
         name='patient-medical-records'),

    # Create a new medical record for a patient
    path('patients/<int:patient_id>/medical-records/create/',
         records_view.create_medical_record,
         name='create-medical-record'),

    # Update an existing medical record
    path('medical-records/<int:record_id>/update/',
         records_view.update_medical_record,
         name='update-medical-record'),

    # Delete a medical record
    path('medical-records/<int:record_id>/delete/',
         records_view.delete_medical_record,
         name='delete-medical-record'),
     
         path('staff/add/',
         staff_view.create_staff_member,
         name='add-staff-member'),

    path('staff/<int:user_id>/',
         staff_view.get_staff_by_user_id,
         name='get-staff-by-user-id'),

    path('staff/list', staff_view.list_all_staff, name='list_all_staff'),
    path('staff/update/<int:user_id>', staff_view.update_staff_member, name='update_staff_member'),
    path('staff/delete/<int:staff_id>/<str:role_name>', staff_view.delete_staff_member, name='delete_staff_member'),

     # Inventory Management
    # Category URLs
    path('categories/', category_view.category_list, name='list-all-categories'),
    path('categories/create/', category_view.category_create, name='create-category'),
    path('categories/<int:pk>/', category_view.category_detail, name='category-details'),

    # Supplier URLs
    path('suppliers/', supplier_view.supplier_list, name='list-all-suppliers'),
    path('suppliers/create/', supplier_view.supplier_create, name='create-supplier'),
    path('suppliers/<int:pk>/', supplier_view.supplier_detail, name='supplier-details'),

    # Inventory URLs
    path('inventory/', inventory_views.inventory_list, name='list-all-items'),
    path('inventory/create/', inventory_views.inventory_create, name='create-item'),
    path('inventory/<int:pk>/', inventory_views.inventory_detail, name='item-details'),
    path('inventory/<int:pk>/update-stock/', inventory_views.update_stock, name='update-item-stock'),

    # Log URLs
    path('logs/', log_views.log_list, name='list-all-logs'),
    
    # Surgery Management
    # Admin Surgery URLs
    path('A/surgeries/', A_surgery_views.get_all_surgeries, name='get-all-surgeries'),
    path('A/surgeries/create/', A_surgery_views.create_surgery, name='create-surgery'),
    path('A/surgeries/<int:surgery_id>/', A_surgery_views.get_surgery, name='get-surgery'),
    path('A/surgeries/<int:surgery_id>/update/', A_surgery_views.update_surgery, name='update-surgery'),
    path('A/surgeries/<int:surgery_id>/delete/', A_surgery_views.delete_surgery, name='delete-surgery'),
    path('A/surgeries/doctor/<int:doctor_id>/', A_surgery_views.get_surgeries_by_doctor, name='get-surgeries-by-doctor'),
    path('A/surgeries/room/<int:room_id>/', A_surgery_views.get_surgeries_by_room, name='get-surgeries-by-room'),
    path('A/surgeries/department/<int:department_id>/', A_surgery_views.get_surgeries_by_department, name='get-surgeries-by-department'),
    path('A/surgeries/upcoming/', A_surgery_views.get_upcoming_surgeries, name='get-upcoming-surgeries'),
    path('A/surgeries/room-availability/<int:room_id>/<str:start_time>/<str:end_time>/', 
         A_surgery_views.check_room_availability, name='check-room-availability'),
    path('A/surgeries/statistics/', A_surgery_views.get_surgery_statistics, name='get-surgery-statistics'),
    path('A/surgeries/by-status/<str:status>/',  A_surgery_views.get_surgeries_by_status, name='surgeries-by-status'),
    
    # Surgery Type URLs
    path('surgery-types/', A_surgery_type_views.get_all_surgery_types, name='get-all-surgery-types'),
    path('surgery-types/create/', A_surgery_type_views.create_surgery_type, name='create-surgery-type'),
    path('surgery-types/department/<int:department_id>/', A_surgery_type_views.get_surgery_types_by_department, name='get-surgery-types-by-department'),
    path('surgery-types/<int:type_id>/', W_surgery_views.get_surgery_type_details, name='surgery-type-details'),
    
    # Doctor Surgery URLs
    path('W/surgeries/doctor/<int:doctor_id>', W_surgery_views.get_surgeries, name='get-all-surgeries'),
    path('W/surgeries/schedule/', W_surgery_views.schedule_surgery, name='create-surgery'),
    path('W/surgeries/<int:surgery_id>/complete/', W_surgery_views.complete_surgery, name='complete-surgery'),

    path('consultations/', consultation_view.get_consultations, name='consultations-list'),
    path('consultations/<int:pk>/', consultation_view.get_consultation, name='consultation-detail'),
    path('consultations/create/', consultation_view.create_consultation, name='consultation-create'),
    path('consultations/<int:pk>/update/', consultation_view.update_consultation, name='consultation-update'),
    path('consultations/<int:pk>/delete/', consultation_view.delete_consultation, name='consultation-delete'),

    path('api/billing/', billing_view.billing_list, name='billing-list'),
    path('api/billing/<int:pk>/', billing_view.billing_detail, name='billing-detail'),
    path('api/billing/create/', billing_view.billing_create, name='billing-create'),
    path('api/billing/<int:pk>/update/', billing_view.billing_update, name='billing-update'),
    path('api/billing/<int:pk>/delete/', billing_view.billing_delete, name='billing-delete'),
    path('api/billing/<int:pk>/print/', billing_view.print_invoice, name='billing-print'),

]