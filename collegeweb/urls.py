"""
URL configuration for collegeweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import edit_profile

urlpatterns = [

# Homepage
    path('homepage/', views.home, name='home'),
    path('home-library/', views.home_library, name='home_library'),
    path('category/<str:category_key>/', views.category_books, name='category_books'),
    path('admission/', views.admission, name='admission'),
    path('validate-field/', views.validate_field, name='validate_field'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('courses/', views.courses, name='courses'),
    path('campus/', views.campus, name='campus'),
    path('enquiry/', views.enquiry_view, name='enquiry'), 


# Admin
    path('admin/', admin.site.urls),
    path('dashboard/login/', views.custom_admin_login, name='custom_admin_login'), 
    path('dashboard/logout/', views.custom_admin_logout, name='custom_admin_logout'),
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-grievances/', views.manage_grievances, name='manage_grievances'),
    path('student-options/', views.student_options, name='student_options'),
    path('faculty-options/', views.faculty_options, name='faculty_options'),
        # Manage library
            path('library/', views.manage_library, name='manage_library'),
            path('toggle-availability/<int:book_id>/', views.toggle_book_availability, name='toggle_book_availability'),
            path('add-library-book/', views.add_library_book, name='add_library_book'),
            path('edit-library-book/<int:id>/', views.edit_library_book, name='edit_library_book'),
            path('delete-library-book/<int:id>/', views.delete_library_book, name='delete_library_book'),
        # Manage Application
            path('applications/', views.manage_applications, name='manage_applications'),
            path('application/<int:application_id>/', views.view_application, name='view_application'),
            path('delete-application/<int:id>/', views.delete_application, name='delete_application'),
        # Manage enquiry
            path('enquiries/', views.manage_enquiries, name='manage_enquiries'),
            path('view-enquiry/<int:id>/', views.view_enquiry, name='view_enquiry'),
            path('delete-enquiry/<int:id>/', views.delete_enquiry, name='delete_enquiry'),

    # Manage students
            path('add-student/', views.add_student, name='add_student'),
            path('custom-admin/students/', views.manage_students, name='manage_students'),
            path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
            path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
        # Academic Details
            path('academic-details/', views.academic_details, name='academic_details'),
            path('add-academic-details/', views.add_academic_details, name='add_academic_details'),
            path('edit-academic-details/<int:id>/', views.edit_academic_details, name='edit_academic_details'),
            path('delete-academic-details/<int:id>/', views.delete_academic_details, name='delete_academic_details'),
        # Attendance
            path('attendance_list/', views.attendance, name='attendance_list'),
            path('attendance/add/', views.admn_std_attendance, name='admn_std_add_attendance'),
            path('edit-attendance/<int:id>/', views.edit_attendance, name='edit_attendance'),
            path('delete-attendance/<int:id>/', views.delete_attendance, name='delete_attendance'),
         # Fee
            path('fee/', views.fee, name='fee'),
            path('add-fee/', views.add_fee, name='add_fee'),
            path('edit-fee/<int:id>/', views.edit_fee, name='edit_fee'),
            path('delete-fee/<int:id>/', views.delete_fee, name='delete_fee'),
        # Certificates
            path('certificates/', views.certificates, name='certificates'),
            path('add-certificate/', views.add_certificate, name='add_certificate'),
            path('edit-certificate/<int:id>/', views.edit_certificate, name='edit_certificate'),
            path('delete-certificate/<int:id>/', views.delete_certificate, name='delete_certificate'),

    # Manage faculty
            path('custom-admin/faculty/', views.manage_faculty, name='manage_faculty'),
            path('add-faculty/', views.add_faculty, name='add_faculty'),
            path('edit-faculty/<int:faculty_id>/', views.edit_faculty, name='edit_faculty'),
            path('delete-faculty/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),
        # Manage salary
            path('salary/', views.salary, name='salary'),
            path('add-salary/', views.add_salary, name='add_salary'),
            path('edit-salary/<int:id>/', views.edit_salary, name='edit_salary'),
            path('delete-salary/<int:id>/', views.delete_salary, name='delete_salary'),
        # Manage attendance
            path('fac_attendance/', views.fac_attendance, name='fac_attendance'),
            path('add-faculty-attendance/', views.add_faculty_attendance, name='add_faculty_attendance'),
            path('edit-faculty-attendance/<int:id>/', views.edit_faculty_attendance, name='edit_faculty_attendance'),
            path('delete-faculty-attendance/<int:id>/', views.delete_faculty_attendance, name='delete_faculty_attendance'),
        # Manage courseplan
            path('course_plan/', views.course_plan, name='course_plan'),
            path('add-course-planning/', views.add_course_planning, name='add_course_planning'),
            path('edit-course-planning/<int:id>/', views.edit_course_planning, name='edit_course_planning'),
            path('delete-course-planning/<int:id>/', views.delete_course_planning, name='delete_course_planning'),


# faculty dashboard
path('fac_login/', views.fac_login, name="fac_loginpage"),
path('facdash/', views.fac_dash, name="facdash"),
path('edit_faculty_profile/<int:faculty_id>/', views.edit_faculty_profile, name='edit_faculty_profile'),
path('salary-details/', views.salary_details, name='salary_details'),
path('attendance/teachers/', views.faculty_attendance, name='faculty_attendance'),
path('faculty/manage-student-attendance/', views.manage_student_attendance, name='manage_student_attendance'),
path('fac-std-attendance/add/', views.add_attendance, name='add_attendance'),
path('faculty/academic/details/', views.faculty_academic_details, name='faculty_academic_details'),
path('faculty/academic/edit/<int:id>/', views.faculty_edit_academic_details, name='faculty_edit_academic_details'),
path('view_grievances/', views.view_grievances, name='view_grievances'),
path('academics/', views.course_planning, name='course_planning'),
path('faculty/logout/', views.fac_logout, name='fac_logout'),


# student dashboard
path('std_login/', views.std_login, name="std_loginpage"), 
path('stddash/', views.std_dash, name="stddash"),
path('edit_profile/<int:student_id>/', edit_profile, name='edit_profile'),
path('academic-progress/', views.academic_progress, name='academic_progress'),
path('attendance/', views.attendance_view, name='attendance'),
path('fee_details/', views.fee_details_view, name='fee_details'),
path('std_certificates/', views.certificates_view, name='std_certificates'),
path('grievance/', views.grievance_page, name='grievance'),
path('student/logout/', views.std_logout, name='std_logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)