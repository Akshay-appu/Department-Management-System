from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.contrib import messages  
from .models import *
from .models import Application
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password  
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta, date
from collections import defaultdict
from django.db.models.functions import TruncDate








############################################## HOMEPAGE ###########################################################
############################################## HOMEPAGE ###########################################################
############################################## HOMEPAGE ###########################################################


# homepage
def home(request):
    return render(request, 'home.html')

# courses
def courses(request):
    return render(request, 'courses.html')

# campus gallery
def campus(request):
    return render(request, 'campus.html')

def home_library(request):
    featured_books = Library.objects.filter(is_available=True)[:4]  # Fetch top 4 available books
    return render(request, 'library.html', {'featured_books': featured_books})

def category_books(request, category_key):
    status = request.GET.get('status', 'all')  
    
    books = Library.objects.filter(category_key=category_key)
    
    if status == 'available':
        books = books.filter(is_available=True)
    elif status == 'unavailable':
        books = books.filter(is_available=False)
    
    return render(request, 'category_books.html', {'books': books})

# Enquiry
def enquiry_view(request):
    if request.method == "POST":
        # Get form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Check if all fields are provided
        if name and email and message:
            # Create a new Enquiry record in the database
            enquiry = Enquiry.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, "Your enquiry has been submitted successfully!")
            return redirect('home') 
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'home.html')

# Application form
def admission(request):
    if request.method == "POST":
        # Collect form data
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        address = request.POST.get('address')
        course = request.POST.get('course')
        documents = request.FILES.get('documents') 

        errors = {}

        # Validate required fields
        if not full_name:
            errors['full_name'] = "Full name is required."
        if not dob:
            errors['dob'] = "Date of birth is required."
        if not email:
            errors['email'] = "A valid email address is required."
        if not phone:
            errors['phone'] = "Phone number is required."
        if not gender:
            errors['gender'] = "Gender is required."
        if not nationality:
            errors['nationality'] = "Nationality is required."
        if not address:
            errors['address'] = "Address is required."
        if not course:
            errors['course'] = "Course selection is required."
        if not documents:
            errors['documents'] = "Uploaded documents are required."

        # Validate DOB (age >= 18 years)
        if dob:
            try:
                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                today = datetime.today().date()
                age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                if age < 18:
                    errors['dob'] = "You must be at least 18 years old to apply."
            except ValueError:
                errors['dob'] = "Invalid date of birth format. Please use YYYY-MM-DD."

        # Validate duplicate email
        if email and Application.objects.filter(email=email).exists():
            errors['email'] = "This email is already in use. Please use a different email."

        # Validate duplicate phone
        if phone and Application.objects.filter(phone=phone).exists():
            errors['phone'] = "This phone number is already in use. Please use a different phone number."

        # If there are errors, re-render the form with error messages
        if errors:
            return render(request, 'admission.html', {
                'errors': errors,
                'form_data': {
                    'full_name': full_name,
                    'dob': dob,
                    'email': email,
                    'phone': phone,
                    'gender': gender,
                    'nationality': nationality,
                    'address': address,
                    'course': course,
                },
            })

        # Save the application if no errors
        application = Application(
            full_name=full_name,
            dob=dob_date,
            email=email,
            phone=phone,
            gender=gender,
            nationality=nationality,
            address=address,
            course=course,
            documents=documents,
        )
        application.save()
        messages.success(
            request,
            f"Thank you {full_name}! Your application for the {course} course has been submitted successfully. We will contact you soon."
        )
        return redirect('admission')

    return render(request, 'admission.html')

def validate_field(request):
    field_name = request.GET.get('field_name') 
    field_value = request.GET.get('field_value')
    response = {'is_valid': True}

    if field_name == "email":
        if Application.objects.filter(email=field_value).exists():
            response = {
                'is_valid': False,
                'error': "This email is already in use. Please use a different email."
            }
    elif field_name == "phone":
        if Application.objects.filter(phone=field_value).exists():
            response = {
                'is_valid': False,
                'error': "This phone number is already in use. Please use a different phone number."
            }
    
    return JsonResponse(response)

# Chatbot
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()  # Convert to lowercase for case-insensitive matching

        # Predefined responses
        responses = {
            "hi": "Hi there! How can I help you today?",
        }

        default_response = "I'm sorry, I didn't understand that. Please try asking differently."
        bot_response = default_response  # Default response
        for key, response in responses.items():
            if key in user_message:  # Check if keyword exists in the message
                bot_response = response
                break

        return JsonResponse({'response': bot_response})
    


############################################## ADMiN ###########################################################
############################################## ADMiN ###########################################################
############################################## ADMiN ###########################################################


# Login Page
ADMIN_USERNAME = "akshay"
ADMIN_PASSWORD = "admin123"

def custom_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Save session data to mark the user as logged in
            request.session['is_admin_logged_in'] = True
            messages.success(request, "Logged in successfully!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    return render(request, 'admin/login.html')

def custom_admin_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('custom_admin_login')

def admin_dashboard(request):
    if not request.session.get('is_admin_logged_in'):
        messages.error(request, "You must log in to access the admin dashboard.")
        return redirect('custom_admin_login')

    return render(request, 'admin/admin_dashboard.html')


def student_options(request):
    return render(request, 'admin/student_options.html')

def faculty_options(request):
    return render(request, 'admin/faculty_options.html')


# Manage Library
def manage_library(request):
    status = request.GET.get('status', 'all')  # Default to 'all' if no filter is specified
    search_query = request.GET.get('search', '').strip()  # General search query

    books = Library.objects.all()

    # Apply status filter
    if status == 'available':
        books = books.filter(is_available=True)
    elif status == 'unavailable':
        books = books.filter(is_available=False)

    # Apply general search filter
    if search_query:
        books = books.filter(
            models.Q(category_key__icontains=search_query) |
            models.Q(name__icontains=search_query) |
            models.Q(author__icontains=search_query)
        )

    return render(request, 'admin/library/library.html', {
        'books': books,
        'status': status,
        'search': search_query,
    })


def toggle_book_availability(request, book_id):
    # Fetch the book object using the provided book_id
    book = get_object_or_404(Library, id=book_id)
    
    # Toggle the is_available field
    book.is_available = not book.is_available
    book.save()
    
    # Redirect back to the manage library page
    return redirect('manage_library')  # Replace 'manage_library' with your actual URL name    

def add_library_book(request):
    # Fetch distinct category keys from the Library table
    categories = Library.objects.values('category_key').distinct()

    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        category_key = request.POST.get('category_key')
        new_category_key = request.POST.get('new_category_key')
        image = request.FILES.get('image')  # Handle file upload

        # If the user entered a new category, use that; otherwise, use the selected one
        if new_category_key:
            category_key = new_category_key

        # Create a new Library record
        book = Library(
            name=name,
            author=author,
            category_key=category_key,
            image=image  # Save the uploaded image
        )
        book.save()

        messages.success(request, "Book added successfully!")
        return redirect('manage_library')

    return render(request, 'admin/library/add_library_book.html', {'categories': categories})

def edit_library_book(request, id):
    book = get_object_or_404(Library, id=id)

    # Fetch distinct category keys
    categories = Library.objects.values('category_key').distinct()

    if request.method == 'POST':
        book.name = request.POST.get('name')
        book.author = request.POST.get('author')
        book.category_key = request.POST.get('category_key')

        # Handle image upload
        if 'image' in request.FILES:
            book.image = request.FILES['image']

        book.save()
        messages.success(request, "Book updated successfully!")
        return redirect('manage_library')

    return render(request, 'admin/library/edit_library_book.html', {
        'book': book,
        'categories': categories
    })

def delete_library_book(request, id):
    book = get_object_or_404(Library, id=id)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('manage_library')

# Admin manage grievances
def manage_grievances(request):
    grievances = Grievance.objects.all()  
    
    if request.method == 'POST':
        grievance_id = request.POST.get('grievance_id')
        grievance = Grievance.objects.get(id=grievance_id)
        response = request.POST.get('response')
        
        # Mark grievance as resolved and store the response
        grievance.status = 'Resolved'
        grievance.response = response
        # grievance.resolved_by = request.user  # Set the current user (admin/faculty) as the one who resolved it
        grievance.save()

        return redirect('manage_grievances')  
    
    return render(request, 'admin/manage_grievances.html', {'grievances': grievances})

# Manage Applications
def manage_applications(request):
    applications = Application.objects.all()
    context = {
        'applications': applications
    }
    return render(request, 'admin/admission/applications_list.html', context)

def view_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    return render(request, 'admin/admission/application_detail.html', {'application': application})

def delete_application(request, id):
    application = get_object_or_404(Application, id=id)
    application.delete()
    messages.success(request, "Application deleted successfully!")
    return redirect('manage_applications')


# Manage enquiry
def manage_enquiries(request):
    enquiries = Enquiry.objects.all()  
    return render(request, 'admin/enquiry/enquiries_list.html', {'enquiries': enquiries})

def view_enquiry(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)
    return render(request, 'admin/enquiries/view_enquiry.html', {'enquiry': enquiry})

def delete_enquiry(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)
    enquiry.delete()
    messages.success(request, "Enquiry deleted successfully!")
    return redirect('manage_enquiries')


############################################ ADMIN'S STUDENT SECTION ###########################################################

# Manage students section
def manage_students(request):
    students_list = students.objects.all().order_by('id')  
    context = {'students': students_list}
    return render(request, 'admin/student/manage_students/manage_students.html', context)

def add_student(request):
    if request.method == 'POST':
        # Get data from the POST request
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        address = request.POST.get('address')
        course = request.POST.get('course')
        documents = request.FILES.get('documents')  
        password = request.POST.get('password')  
        password2 = request.POST.get('password2')  

        # Check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('add_student')

        # Hash the password before saving it
        hashed_password = make_password(password)

        # Create a new student record
        student = students(
            full_name=full_name,
            dob=dob,
            email=email,
            phone=phone,
            gender=gender,
            nationality=nationality,
            address=address,
            course=course,
            documents=documents,
            password=hashed_password  
        )
        student.save()
        messages.success(request, "Student added successfully!")
        return redirect('manage_students')  

    return render(request, 'admin/student/manage_students/add_student.html')

def edit_student(request, student_id):
    student = get_object_or_404(students, id=student_id)

    if request.method == 'POST':
        # Update student fields
        student.full_name = request.POST.get('full_name')
        student.dob = request.POST.get('dob')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.gender = request.POST.get('gender')
        student.nationality = request.POST.get('nationality')
        student.address = request.POST.get('address')
        student.course = request.POST.get('course')

        # Handle file uploads (documents and photo)
        if 'documents' in request.FILES:
            student.documents = request.FILES['documents']
        
        if 'photo' in request.FILES:
            student.photo = request.FILES['photo']

        # Handle password update if provided
        password = request.POST.get('password')
        if password:
            password2 = request.POST.get('password2')
            if password != password2:
                messages.error(request, "Passwords do not match!")
                return redirect('edit_student', student_id=student.id)
            student.password = make_password(password)

        student.save()  # Save the updated student object
        messages.success(request, "Student updated successfully!")

        return redirect('manage_students')  

    context = {'student': student}
    return render(request, 'admin/student/manage_students/edit_student.html', context)

def delete_student(request, student_id):
    student = get_object_or_404(students, id=student_id)
    student.delete()
    messages.success(request, f"Student {student.full_name} has been successfully deleted.")

    return redirect('manage_students')


# Manage Academic Details
def academic_details(request):
    details = AcademicDetails.objects.all()

    # Add attendance percentage for each student's academic details
    for detail in details:
        detail.attendance_percentage = detail.calculate_attendance_percentage()

    return render(request, 'admin/student/academic/academic_details.html', {'details': details})

def add_academic_details(request):
    students_list = students.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        gpa = request.POST.get('gpa')
        attendance = request.POST.get('attendance')
        subject_1 = request.POST.get('subject_1')
        marks_1 = request.POST.get('marks_1')
        subject_2 = request.POST.get('subject_2')
        marks_2 = request.POST.get('marks_2')
        subject_3 = request.POST.get('subject_3')
        marks_3 = request.POST.get('marks_3')
        subject_4 = request.POST.get('subject_4')
        marks_4 = request.POST.get('marks_4')
        subject_5 = request.POST.get('subject_5')
        marks_5 = request.POST.get('marks_5')
        remarks = request.POST.get('remarks')

        student = students.objects.get(id=student_id)

        academic_detail = AcademicDetails(
            student=student,
            gpa=gpa,
            attendance=attendance,
            subject_1=subject_1,
            marks_1=marks_1,
            subject_2=subject_2,
            marks_2=marks_2,
            subject_3=subject_3,
            marks_3=marks_3,
            subject_4=subject_4,
            marks_4=marks_4,
            subject_5=subject_5,
            marks_5=marks_5,
            remarks=remarks
        )
        academic_detail.save()
        messages.success(request, "New academic details added successfully!")
        return redirect('academic_details')

    return render(request, 'admin/student/academic/add_academic_details.html', {'students': students_list})

def edit_academic_details(request, id):
    detail = get_object_or_404(AcademicDetails, id=id)

    if request.method == 'POST':
        detail.gpa = request.POST.get('gpa')
        detail.attendance = request.POST.get('attendance')
        detail.subject_1 = request.POST.get('subject_1')
        detail.marks_1 = request.POST.get('marks_1')
        detail.subject_2 = request.POST.get('subject_2')
        detail.marks_2 = request.POST.get('marks_2')
        detail.subject_3 = request.POST.get('subject_3')
        detail.marks_3 = request.POST.get('marks_3')
        detail.subject_4 = request.POST.get('subject_4')
        detail.marks_4 = request.POST.get('marks_4')
        detail.subject_5 = request.POST.get('subject_5')
        detail.marks_5 = request.POST.get('marks_5')
        detail.remarks = request.POST.get('remarks')
        
        detail.save()
        messages.success(request, "Academic details updated successfully!")
        return redirect('academic_details')
    return render(request, 'admin/student/academic/edit_academic_details.html', {'detail': detail})

def delete_academic_details(request, id):
    detail = get_object_or_404(AcademicDetails, id=id)
    detail.delete()
    messages.success(request, "Academic details deleted successfully!")
    return redirect('academic_details')


# Manage attendance records
def attendance(request):
    # Get all students for the dropdown
    all_students = students.objects.all()

    # Initialize filter values
    selected_student_id = request.GET.get('student')
    selected_single_date = request.GET.get('single_date')
    selected_start_date = request.GET.get('start_date')
    selected_end_date = request.GET.get('end_date')

    # Build the filter condition
    filter_condition = Q()

    if selected_student_id:
        filter_condition &= Q(student_id=selected_student_id)
    if selected_single_date:
        filter_condition &= Q(date=selected_single_date)
    if selected_start_date and selected_end_date:
        filter_condition &= Q(date__gte=selected_start_date, date__lte=selected_end_date)

    # Apply the filter to Attendance records and order by date descending (newest first)
    attendance_records = Attendance.objects.filter(filter_condition).order_by('-date')

    # Render the template with the filtered records and filter values
    return render(request, 'admin/student/attendance/attendance_list.html', {
        'attendance_records': attendance_records,
        'all_students': all_students,
        'selected_student_id': selected_student_id,
        'selected_single_date': selected_single_date,
        'selected_start_date': selected_start_date,
        'selected_end_date': selected_end_date,
    })

def admn_std_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        attendance_date = request.POST.get('attendance_date')

        # Ensure student and date are provided
        if student_id and attendance_date:
            student = students.objects.get(id=student_id)
            attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
            
            # Check if attendance already exists for the same date and student
            if not Attendance.objects.filter(student=student, date=attendance_date).exists():
                Attendance.objects.create(student=student, date=attendance_date)
                return redirect('attendance_list')  # Redirect to the attendance list page
            else:
                return HttpResponse("Attendance for this student on this date already exists.", status=400)
    
    # Fetch all students for the dropdown
    all_students = students.objects.all()
    return render(request, 'admin/student/attendance/admn_std_add_attendance.html', {'all_students': all_students})

def edit_attendance(request, id):
    attendance_record = get_object_or_404(Attendance, id=id)

    if request.method == 'POST':
        attendance_record.date = request.POST.get('date')
        attendance_record.attendance_percentage = request.POST.get('attendance_percentage')
        attendance_record.save()
        messages.success(request, "Attendance updated successfully!")
        return redirect('attendance_list')

    return render(request, 'admin/student/attendance/edit_attendance.html', {'attendance_record': attendance_record})

def delete_attendance(request, id):
    attendance_record = get_object_or_404(Attendance, id=id)
    attendance_record.delete()
    messages.success(request, "Attendance record deleted successfully!")
    return redirect('attendance_list')


# Managefee records
def fee(request):
    fee_records = Fee.objects.all()  
    return render(request, 'admin/student/fee/fee_list.html', {'fee_records': fee_records})

def add_fee(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        total_fee = request.POST.get('total_fee')
        paid_fee = request.POST.get('paid_fee')
        due_fee = request.POST.get('due_fee')
        due_date = request.POST.get('due_date')  

        student = students.objects.get(id=student_id)

        fee_record = Fee(
            student=student,
            total_fee=total_fee,
            paid_fee=paid_fee,
            due_fee=due_fee,
            due_date=due_date  
        )
        fee_record.save()
        messages.success(request, "Fee details added successfully!")
        return redirect('fee')  

    # Pass the list of students to the template for the select dropdown
    students_list = students.objects.all()
    return render(request, 'admin/student/fee/add_fee.html', {'students': students_list})

def edit_fee(request, id):
    fee_record = get_object_or_404(Fee, id=id)

    if request.method == 'POST':
        fee_record.total_fee = request.POST.get('total_fee')
        fee_record.paid_fee = request.POST.get('paid_fee')
        fee_record.due_fee = request.POST.get('due_fee')
        fee_record.due_date = request.POST.get('due_date')  
        fee_record.save()
        messages.success(request, "Fee details updated successfully!")
        return redirect('fee')  

    return render(request, 'admin/student/fee/edit_fee.html', {'fee_record': fee_record})

def delete_fee(request, id):
    fee_record = get_object_or_404(Fee, id=id)
    fee_record.delete()
    messages.success(request, "Fee record deleted successfully!")
    return redirect('fee')


# Manage certificates
def certificates(request):
    certificate_records = Certificate.objects.all() 
    return render(request, 'admin/student/certificates/certificates_list.html', {'certificate_records': certificate_records})

def add_certificate(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        certificate_name = request.POST.get('certificate_name')
        issued_by = request.POST.get('issued_by')
        issue_date = request.POST.get('issue_date')

        # Get the selected student object
        student = students.objects.get(id=student_id)

        # Create new Certificate record
        certificate = Certificate(
            student=student,
            certificate_name=certificate_name,
            issued_by=issued_by,
            issue_date=issue_date
        )
        certificate.save()
        messages.success(request, "Certificate added successfully!")
        return redirect('certificates')

    # Pass the list of students to the template for the select dropdown
    students_list = students.objects.all()
    return render(request, 'admin/student/certificates/add_certificate.html', {'students': students_list})

def edit_certificate(request, id):
    certificate_record = get_object_or_404(Certificate, id=id)

    if request.method == 'POST':
        certificate_record.certificate_name = request.POST.get('certificate_name')
        certificate_record.issued_by = request.POST.get('issued_by')
        certificate_record.issue_date = request.POST.get('issue_date')
        certificate_record.save()
        messages.success(request, "Certificate updated successfully!")
        return redirect('certificates')

    return render(request, 'admin/student/certificates/edit_certificate.html', {'certificate_record': certificate_record})

def delete_certificate(request, id):
    certificate_record = get_object_or_404(Certificate, id=id)
    certificate_record.delete()
    messages.success(request, "Certificate deleted successfully!")
    return redirect('certificates')


############################################ ADMIN'S FACULTY SECTION #######################################################

# Manage Faculty
def manage_faculty(request):
    faculties_list = faculties.objects.all().order_by('faculty_id')
    context = {
        'faculties': faculties_list,
    }

    return render(request, 'admin/faculty/manage_faculty/manage_faculty.html', context)

def add_faculty(request):
    if request.method == 'POST':
        # Get data from the POST request
        faculty_id = request.POST.get('faculty_id')  
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        photo = request.FILES.get('photo')  
        
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('add_faculty')

        hashed_password = make_password(password)

        faculty = faculties(
            faculty_id=faculty_id,
            full_name=full_name,
            email=email,
            phone=phone,
            department=department,
            password=hashed_password,
            photo=photo  
        )
        faculty.save()

        messages.success(request, "Faculty added successfully!")
        return redirect('manage_faculty')  

    return render(request, 'admin/faculty/manage_faculty/add_faculty.html')

def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(faculties, id=faculty_id)

    if request.method == 'POST':
        # Update the faculty's details with submitted data
        faculty.full_name = request.POST.get('full_name')
        faculty.email = request.POST.get('email')
        faculty.phone = request.POST.get('phone')
        faculty.department = request.POST.get('department')

        # Handle password update if provided
        password = request.POST.get('password')
        if password:
            password2 = request.POST.get('password2')
            if password != password2:
                messages.error(request, "Passwords do not match!")
                return redirect('edit_faculty', faculty_id=faculty.id)
            # Hash the new password before saving
            faculty.password = make_password(password)

        # Handle photo update if provided
        photo = request.FILES.get('photo')
        if photo:
            faculty.photo = photo

        faculty.save()  
        messages.success(request, "Faculty updated successfully!")
        return redirect('manage_faculty')

    context = {'faculty': faculty}
    return render(request, 'admin/faculty/manage_faculty/edit_faculty.html', context)   

def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(faculties, id=faculty_id)
    faculty.delete()
    messages.success(request, f"Faculty member {faculty.full_name} has been successfully deleted.")
    return redirect('manage_faculty')


# Manage salary records
def salary(request):
    # Get the faculty_id from the GET parameters
    faculty_id = request.GET.get('faculty_id')
    
    # Fetch all faculties for the dropdown menu
    faculty_list = faculties.objects.all().order_by('id')
    
    # Filter salary records if faculty_id is provided, otherwise fetch all
    if faculty_id:
        salary_records = SalaryDetail.objects.filter(faculty_id=faculty_id).order_by('faculty_id')
    else:
        salary_records = SalaryDetail.objects.all().order_by('faculty_id')
    
    # Render the template with context data
    return render(request, 'admin/faculty/salary/salary_list.html', {
        'salary_records': salary_records,
        'faculty_list': faculty_list,
        'selected_faculty_id': faculty_id  # Pass selected faculty ID for the dropdown
    })

def add_salary(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty')
        salary = request.POST.get('salary')
        month = request.POST.get('month')
        year = request.POST.get('year')
        status = request.POST.get('status')

        # Get the selected faculty object
        faculty = faculties.objects.get(id=faculty_id)

        # Create new SalaryDetail record
        salary_record = SalaryDetail(
            faculty=faculty,
            salary=salary,
            month=month,
            year=year,
            status=status
        )
        salary_record.save()
        messages.success(request, "Salary record added successfully!")
        return redirect('salary')

    # Pass the list of faculties to the template for the select dropdown
    faculties_list = faculties.objects.all()
    return render(request, 'admin/faculty/salary/add_salary.html', {'faculties': faculties_list})

def edit_salary(request, id):
    salary_record = get_object_or_404(SalaryDetail, id=id)

    if request.method == 'POST':
        salary_record.salary = request.POST.get('salary')
        salary_record.month = request.POST.get('month')
        salary_record.year = request.POST.get('year')
        salary_record.status = request.POST.get('status')
        salary_record.save()
        messages.success(request, "Salary record updated successfully!")
        return redirect('salary')

    return render(request, 'admin/faculty/salary/edit_salary.html', {'salary_record': salary_record})

def delete_salary(request, id):
    salary_record = get_object_or_404(SalaryDetail, id=id)
    salary_record.delete()
    messages.success(request, "Salary record deleted successfully!")
    return redirect('salary')


# Managey attendance records
def fac_attendance(request):
    faculty_id = request.GET.get('faculty_id')  # Get faculty ID from GET parameters
    start_date = request.GET.get('start_date')  # Get start date from GET parameters
    end_date = request.GET.get('end_date')  # Get end date from GET parameters
    current_date = date.today()  # Get today's date

    if faculty_id:
        # Get attendance records filtered by faculty ID
        attendance_records = FacultyAttendance.objects.filter(faculty_id=faculty_id)
        selected_faculty = faculties.objects.get(id=faculty_id)
    else:
        # Get all attendance records if no faculty is selected
        attendance_records = FacultyAttendance.objects.all()
        selected_faculty = None

    # Apply date filters if provided
    if start_date and end_date:
        attendance_records = attendance_records.filter(date__range=[start_date, end_date])
    elif start_date:
        attendance_records = attendance_records.filter(date__gte=start_date)
    elif end_date:
        attendance_records = attendance_records.filter(date__lte=end_date)

    # Get all faculties for the dropdown
    faculty_list = faculties.objects.all()

    # Filter records for today's date
    todays_attendance = FacultyAttendance.objects.filter(date=current_date)
    
    return render(request, 'admin/faculty/attendance/fac_attendance_list.html', {
        'attendance_records': attendance_records,
        'faculty_list': faculty_list,
        'selected_faculty_id': faculty_id,
        'selected_faculty': selected_faculty,
        'todays_attendance': todays_attendance,  # Passing today's attendance data
        'current_date': current_date  # Passing today's date to the template
    })

def add_faculty_attendance(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty')
        date = request.POST.get('date')
        status = request.POST.get('status')

        # Get the selected faculty object
        faculty = faculties.objects.get(id=faculty_id)

        # Create new FacultyAttendance record
        attendance_record = FacultyAttendance(
            faculty=faculty,
            date=date,
            status=status
        )
        attendance_record.save()
        messages.success(request, "Attendance record added successfully!")
        return redirect('fac_attendance')

    # Pass the list of faculties to the template for the select dropdown
    faculties_list = faculties.objects.all()
    return render(request, 'admin/faculty/attendance/add_attendance.html', {'faculties': faculties_list})

def edit_faculty_attendance(request, id):
    attendance_record = get_object_or_404(FacultyAttendance, id=id)

    if request.method == 'POST':
        attendance_record.date = request.POST.get('date')
        attendance_record.status = request.POST.get('status')
        attendance_record.save()
        messages.success(request, "Attendance record updated successfully!")
        return redirect('fac_attendance')

    return render(request, 'admin/faculty/attendance/edit_attendance.html', {'attendance_record': attendance_record})

def delete_faculty_attendance(request, id):
    attendance_record = get_object_or_404(FacultyAttendance, id=id)
    attendance_record.delete()
    messages.success(request, "Attendance record deleted successfully!")
    return redirect('fac_attendance')

# Manage courseplan 
def course_plan(request):
    plans = CoursePlanning.objects.all()  # Get all course plans
    return render(request, 'admin/faculty/course_planning/course_planning_list.html', {'plans': plans})

def add_course_planning(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty')
        subject_name = request.POST.get('subject_name')
        timing = request.POST.get('timing')
        study_plan = request.POST.get('study_plan')

        # Get the selected faculty object
        faculty = faculties.objects.get(id=faculty_id)

        # Create new CoursePlanning record
        plan = CoursePlanning(
            faculty=faculty,
            subject_name=subject_name,
            timing=timing,
            study_plan=study_plan
        )
        plan.save()
        messages.success(request, "Course plan added successfully!")
        return redirect('course_plan')

    # Pass the list of faculties to the template for the select dropdown
    faculties_list = faculties.objects.all()
    return render(request, 'admin/faculty/course_planning/add_course_planning.html', {'faculties': faculties_list})

def edit_course_planning(request, id):
    plan = get_object_or_404(CoursePlanning, id=id)

    if request.method == 'POST':
        plan.subject_name = request.POST.get('subject_name')
        plan.timing = request.POST.get('timing')
        plan.study_plan = request.POST.get('study_plan')
        plan.save()
        messages.success(request, "Course plan updated successfully!")
        return redirect('course_plan')  

    return render(request, 'admin/faculty/course_planning/edit_course_planning.html', {'plan': plan})

def delete_course_planning(request, id):
    plan = get_object_or_404(CoursePlanning, id=id)
    plan.delete()
    messages.success(request, "Course plan deleted successfully!")
    return redirect('course_plan')



############################################## STUDENT DASHBOARD FUNCTIONS ###########################################################
############################################## STUDENT DASHBOARD FUNCTIONS ###########################################################
############################################## STUDENT DASHBOARD FUNCTIONS ###########################################################

# student login
def std_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            student = students.objects.get(email=email)

            # Check the password
            if student.password == password:
                # Save the email in the session
                request.session['student_email'] = student.email
                
                return redirect('/stddash/')  
            else:
                # Invalid password
                return render(request, 'student/std_login.html', {'error': 'Invalid email or password.'})
        except students.DoesNotExist:
            # Student not found
            return render(request, 'student/std_login.html', {'error': 'Student not found.'})
    else:
        return render(request, 'student/std_login.html')

def std_dash(request):
    # Check if the user is logged in
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('std_loginpage')

    try:
        # Fetch the logged-in student's details along with their academic and certificate information
        student_details = students.objects.get(email=student_email)
        academic_details = AcademicDetails.objects.get(student=student_details)
        certificates = Certificate.objects.filter(student=student_details)
    except (students.DoesNotExist, AcademicDetails.DoesNotExist):
        return redirect('std_loginpage')

    # Pass the student's details to the template context
    context = {
        'student': student_details,
        'academic_details': academic_details,
        'certificates': certificates,
    }
    return render(request, 'student/std_dash.html', context)

def std_logout(request):
    try:
        del request.session['student_email']
    except KeyError:
        pass  # If no session exists, do nothing
    
    return HttpResponseRedirect(reverse('std_loginpage')) 


# Edit Profile
def edit_profile(request, student_id):
    student = get_object_or_404(students, id=student_id)
    
    if request.method == 'POST':
        # Update the student's details with submitted data
        student.full_name = request.POST.get('full_name')
        student.dob = request.POST.get('dob')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.gender = request.POST.get('gender')
        student.nationality = request.POST.get('nationality')
        student.address = request.POST.get('address')
        student.course = request.POST.get('course')

        if 'documents' in request.FILES:
            student.documents = request.FILES['documents']
        
        if 'photo' in request.FILES:
            student.photo = request.FILES['photo']

        student.save()
        messages.success(request, "Profile updated successfully!")

        return redirect('stddash')

    context = {'student': student}
    return render(request, 'student/edit_profile.html', context)

def academic_progress(request):
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('std_login')  # Redirect to login page if not logged in

    # Fetch the student's academic details
    student = get_object_or_404(students, email=student_email)
    academic_details = get_object_or_404(AcademicDetails, student=student)

    # Calculate GPA and Grade dynamically
    gpa = academic_details.calculate_gpa()
    grade = academic_details.calculate_grade()

    # Calculate GPA as percentage (out of 10, so multiply by 10)
    gpa_percentage = gpa * 10

    # Calculate attendance percentage for the current month
    attendance_percentage = academic_details.calculate_attendance_percentage()

    # Pass details to the template
    context = {
        'student': student,
        'academic_details': academic_details,
        'grade': grade,
        'gpa_percentage': gpa_percentage,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'student/academic_progress.html', context)

# Attendance View
def attendance_view(request):
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('std_login')

    student = students.objects.get(email=student_email)
    attendances = Attendance.objects.filter(student=student)

    # Group attendance by month
    grouped_attendance = defaultdict(list)
    for attendance in attendances:
        month = attendance.date.strftime('%B %Y')  # Format as "Month Year" (e.g., "August 2023")
        grouped_attendance[month].append(attendance.date.day)  # Append the day of the month

    # Calculate attendance count per month
    attendance_summary = [
        {"month": month, "dates": sorted(dates), "count": len(dates)}
        for month, dates in grouped_attendance.items()
    ]

    context = {
        'student': student,
        'attendance_summary': attendance_summary,
    }
    return render(request, 'student/attendance.html', context)

# Fee Details View
def fee_details_view(request):
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('std_login')

    student = students.objects.get(email=student_email)
    fee_details = Fee.objects.filter(student=student)

    context = {
        'student': student,
        'fee_details': fee_details
    }
    return render(request, 'student/fee_details.html', context)

# Certificates View
def certificates_view(request):
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('std_login')

    student = students.objects.get(email=student_email)
    certificates = Certificate.objects.filter(student=student)

    context = {
        'student': student,
        'certificates': certificates
    }
    return render(request, 'student/certificates.html', context)

# grievance_
def grievance_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        student_email = request.session.get('student_email')

        if not student_email:
            return redirect('std_loginpage') 

        try:
            student = students.objects.get(email=student_email)
            # Check if a grievance with the same title and description already exists
            if Grievance.objects.filter(student=student, title=title, description=description).exists():
                success_message = "This grievance has already been submitted."
            else:
                Grievance.objects.create(student=student, title=title, description=description)
                success_message = "Your grievance has been submitted successfully."

            grievances = Grievance.objects.filter(student=student)  # Retrieve student grievances
            return render(request, 'student/grievance.html', {'success_message': success_message, 'grievances': grievances})

        except students.DoesNotExist:
            success_message = "Unable to submit grievance. Please try again."
            return render(request, 'student/grievance.html', {'success_message': success_message})

    # Handle GET request
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('std_loginpage')  

    student = students.objects.get(email=student_email)
    grievances = Grievance.objects.filter(student=student)  
    return render(request, 'student/grievance.html', {'grievances': grievances})



############################################## FACULTY DASHBOARD FUNCTIONS ###########################################################
############################################## FACULTY DASHBOARD FUNCTIONS ###########################################################
############################################## FACULTY DASHBOARD FUNCTIONS ###########################################################


#Faculty Login
def fac_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check credentials in the faculties model
        faculty_details = faculties.objects.filter(email=email).first()
        if faculty_details and password == faculty_details.password:  
            # Set session data for the logged-in faculty
            request.session['faculty_id'] = faculty_details.id
            return redirect('facdash')  

        return render(request, 'faculty/fac_login.html', {'status': 'Invalid email or password'})

    return render(request, 'faculty/fac_login.html')

# Faculty Dashboard
def fac_dash(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('fac_loginpage')
    
    faculty = faculties.objects.get(id=faculty_id)
    messages = ["Welcome to the faculty dashboard!"]  
    notices = ["Upcoming seminar on AI scheduled for Dec 1."]  
    return render(request, 'faculty/fac_dash.html', {
        'faculty': faculty,
        'messages': messages,
        'notices': notices,
    })

# faculty logout
def fac_logout(request):
    try:
        del request.session['faculty_id']  # Delete the session to log out
    except KeyError:
        pass  # If there's no faculty_id in the session, do nothing
    
    # Redirect to the login page after logout
    return HttpResponseRedirect(reverse('fac_loginpage'))  


def edit_faculty_profile(request, faculty_id):
    faculty = get_object_or_404(faculties, id=faculty_id)
    
    if request.method == 'POST':
        # Update fields with POST data
        faculty.full_name = request.POST.get('full_name')
        faculty.email = request.POST.get('email')
        faculty.phone = request.POST.get('phone')
        faculty.department = request.POST.get('department')
        
        # Update photo if a new one is uploaded
        if 'photo' in request.FILES:
            faculty.photo = request.FILES['photo']

        faculty.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('facdash')  # Redirect to faculty dashboard
    
    return render(request, 'faculty/edit_profile.html', {'faculty': faculty})

# Salary Details
def salary_details(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('fac_login')

    salary_records = SalaryDetail.objects.filter(faculty_id=faculty_id)
    return render(request, 'faculty/salary_details.html', {'salary_records': salary_records})

# faculty std attendance
def manage_student_attendance(request):
    # Fetch all students for dropdown
    students_list = students.objects.all()

    # Fetch filtering criteria
    selected_student_id = request.GET.get('student_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Filter attendance records
    today = date.today()
    attendance_records = Attendance.objects.all()

    # Apply student and date filters
    if selected_student_id:
        attendance_records = attendance_records.filter(student_id=selected_student_id)
    if start_date and end_date:
        attendance_records = attendance_records.filter(date__range=[start_date, end_date])

    # Sort by current date first, then by other dates (descending order)
    attendance_records = attendance_records.order_by(
        # Prioritize current date and then order descending by date
        '-date'
    ).extra(
        select={'is_today': 'date = %s'}, select_params=[today], order_by=['-is_today', '-date']
    )

    # Delete attendance record
    if request.method == 'POST' and 'delete_attendance' in request.POST:
        attendance_id = request.POST.get('attendance_id')
        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.delete()
        messages.success(request, "Attendance record deleted successfully!")
        return redirect('manage_student_attendance')

    context = {
        'students': students_list,
        'attendance_records': attendance_records,
        'selected_student_id': selected_student_id,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'faculty/manage_student_attendance.html', context)

def add_attendance(request):
    # Get all students for the dropdown
    all_students = students.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        attendance_date = request.POST.get('date')

        if student_id and attendance_date:
            try:
                student = students.objects.get(id=student_id)
                attendance = Attendance(student=student, date=attendance_date)
                attendance.save()
                messages.success(request, 'Attendance added successfully!')
                return redirect('manage_student_attendance')
            except students.DoesNotExist:
                messages.error(request, 'Student not found!')
        else:
            messages.error(request, 'Please select a student and a valid date.')

    return render(request, 'faculty/add_attendance.html', {
        'all_students': all_students
    })

# Faculty Attendance
def faculty_attendance(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('fac_login')  

    # Fetch attendance records for the faculty
    attendance_records = FacultyAttendance.objects.filter(faculty_id=faculty_id)

    # Group attendance by month
    grouped_attendance = defaultdict(list)
    for attendance in attendance_records:
        month = attendance.date.strftime('%B %Y')  # Format as "Month Year" (e.g., "August 2023")
        if attendance.status == 'Present':
            grouped_attendance[month].append(attendance.date.day)  # Append the day of the month

    # Calculate attendance count per month
    attendance_summary = [
        {"month": month, "dates": sorted(dates), "count": len(dates)}
        for month, dates in grouped_attendance.items()
    ]

    # Debugging to verify data
    if not attendance_summary:
        print(f"No attendance records found for faculty_id: {faculty_id}")
    else:
        print(f"Attendance records fetched for faculty_id: {faculty_id}")

    context = {
        'attendance_summary': attendance_summary,
    }
    return render(request, 'faculty/faculty_attendance.html', context)


# Faculty to - Manage Academic Details
@csrf_exempt
def faculty_academic_details(request):
    # Fetch all academic details for students ordered by id in ascending order
    details = AcademicDetails.objects.all().order_by('id')
    
    # Calculate attendance percentage for each student's academic details
    for detail in details:
        detail.attendance_percentage = detail.calculate_attendance_percentage()

    return render(request, 'faculty/academic_details.html', {'details': details})

@csrf_exempt
def faculty_edit_academic_details(request, id):
    # Get the academic details object by ID
    detail = get_object_or_404(AcademicDetails, id=id)

    if request.method == 'POST':
        # Update fields with the new data from the POST request
        detail.gpa = request.POST.get('gpa')
        detail.attendance = request.POST.get('attendance')
        detail.subject_1 = request.POST.get('subject_1')
        detail.marks_1 = request.POST.get('marks_1')
        detail.subject_2 = request.POST.get('subject_2')
        detail.marks_2 = request.POST.get('marks_2')
        detail.subject_3 = request.POST.get('subject_3')
        detail.marks_3 = request.POST.get('marks_3')
        detail.subject_4 = request.POST.get('subject_4')
        detail.marks_4 = request.POST.get('marks_4')
        detail.subject_5 = request.POST.get('subject_5')
        detail.marks_5 = request.POST.get('marks_5')
        detail.remarks = request.POST.get('remarks')
        
        detail.save()
        messages.success(request, "Academic details updated successfully!")
        return redirect('faculty_academic_details')
    
    return render(request, 'faculty/edit_academic_details.html', {'detail': detail})

# view_grievances
def view_grievances(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('fac_login')  

    grievances = Grievance.objects.filter(status='Pending').select_related('student')

    if request.method == "POST":
        grievance_id = request.POST.get('grievance_id')
        response = request.POST.get('response')
        try:
            grievance = Grievance.objects.get(id=grievance_id)
            grievance.status = 'Resolved'
            grievance.response = response
            grievance.save()
        except Grievance.DoesNotExist:
            pass

    return render(request, 'faculty/view_grievances.html', {'grievances': grievances})

# Course Planning
def course_planning(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('fac_login')

    course_plans = CoursePlanning.objects.filter(faculty_id=faculty_id)
    return render(request, 'faculty/course_planning.html', {'course_plans': course_plans})

