from django.db import models 
from django.contrib.auth.models import User 
from django.utils import timezone  
from datetime import datetime


class Library(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category_key = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='library_images/', null=True, blank=True)  # Image upload field
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name



# Enquiry
class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name} ({self.email})"


# Admission
class Application(models.Model):
    full_name = models.CharField(max_length=100)
    dob = models.DateField(default="2000-01-01")  
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="")  
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default="Male"  
    )
    nationality = models.CharField(max_length=50, default="Unknown")  
    address = models.TextField(default="")  
    academic_details = models.TextField(default="Not Provided")  
    course = models.CharField(max_length=50, default="Not Selected")  
    documents = models.FileField(upload_to='documents/', null=True, blank=True)  
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course}"



############################################## STUDENT DASHBOARD MODELS ###########################################################
############################################## STUDENT DASHBOARD MODELS ###########################################################

class students(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    COURSE_CHOICES = [
        ('BTech', 'Computer Science Engineering'),
        ('MTech_Civil', 'Civil Engineering'),
        ('MTech_EEE', 'Electrical and Electronics Engineering'),
        ('MTech_Marine', 'Marine Engineering'),
        ('MTech_AI', 'AI & ML Engineering'),
        ('MTech_Robotics', 'Robotics Engineering'),
    ]
    
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=50)
    address = models.TextField()
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    documents = models.FileField(upload_to='admissions/documents/')
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.full_name} - {self.course}"


class AcademicDetails(models.Model):
    student = models.OneToOneField('students', on_delete=models.CASCADE, related_name='academic_details')
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    attendance = models.FloatField(default=0.0)

    # Subjects and Marks
    subject_1 = models.CharField(max_length=100, null=True, blank=True)
    marks_1 = models.IntegerField(null=True, blank=True)

    subject_2 = models.CharField(max_length=100, null=True, blank=True)
    marks_2 = models.IntegerField(null=True, blank=True)

    subject_3 = models.CharField(max_length=100, null=True, blank=True)
    marks_3 = models.IntegerField(null=True, blank=True)

    subject_4 = models.CharField(max_length=100, null=True, blank=True)
    marks_4 = models.IntegerField(null=True, blank=True)

    subject_5 = models.CharField(max_length=100, null=True, blank=True)
    marks_5 = models.IntegerField(null=True, blank=True)

    remarks = models.TextField(blank=True, null=True)

    def calculate_gpa(self):
        marks = [self.marks_1, self.marks_2, self.marks_3, self.marks_4, self.marks_5]
        valid_marks = [mark for mark in marks if mark is not None]

        if valid_marks:
            # Calculate average marks
            average_marks = sum(valid_marks) / len(valid_marks)

            # Normalize GPA to a 10-point scale (assuming marks are out of 100)
            gpa = average_marks / 10
            self.gpa = round(gpa, 2)  # Update GPA in the model
            self.save()
        else:
            self.gpa = 0.0
            self.save()

        return self.gpa

    def calculate_grade(self):
        """Determine grade based on GPA"""
        self.calculate_gpa()  # Ensure GPA is updated
        if self.gpa >= 9:
            return "A+ (Excellent)"
        elif self.gpa >= 7:
            return "A (Good)"
        elif self.gpa >= 5:
            return "B (Needs Improvement)"
        else:
            return "C (Poor)"

    def calculate_attendance_percentage(self, month=None):
        """
        Calculate attendance percentage for the given month.
        If no month is provided, it calculates for the current month.
        """
        if month is None:
            month = datetime.now().month  # Default to current month
        
        # Get attendance records for the student for the given month
        attendances = self.student.attendances.filter(date__month=month)
        
        # Assume 30 days in a month, adjust based on actual days
        total_days_in_month = 30
        days_present = attendances.count()

        # Calculate attendance percentage
        attendance_percentage = (days_present / total_days_in_month) * 100
        return round(attendance_percentage, 2)

    def __str__(self):
        return f"Academic Details of {self.student.full_name}"
    

class Attendance(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    
    def __str__(self):
        return f"Attendance for {self.student.full_name} on {self.date}"
    

class Fee(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE, related_name='fees')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fee = models.DecimalField(max_digits=10, decimal_places=2)
    due_fee = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(default=timezone.now)  

    def __str__(self):
        return f"Fee details for {self.student.full_name}"


class Certificate(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE, related_name='certificates')
    certificate_name = models.CharField(max_length=200)
    issued_by = models.CharField(max_length=100)
    issue_date = models.DateField()

    def __str__(self):
        return f"Certificate for {self.student.full_name} - {self.certificate_name}"
    
class Grievance(models.Model):
    student = models.ForeignKey('students', on_delete=models.CASCADE, related_name='grievances')
    title = models.CharField(max_length=200)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Status like 'Pending', 'Resolved'
    response = models.TextField(null=True, blank=True)  #
    resolved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='resolved_grievances')  # Track who resolved

    def __str__(self):
        return f"{self.title} - {self.student.full_name}"


############################################## FACULTY DASHBOARD MODELS ###########################################################
############################################## FACULTY DASHBOARD MODELS ###########################################################


class faculties(models.Model):
    faculty_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=50)
    password = models.CharField(max_length=128)  

    # Add ImageField for faculty photo
    photo = models.ImageField(upload_to='faculty_photos/', blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.department})"

class SalaryDetail(models.Model):
    faculty = models.ForeignKey(faculties, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=15)
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[('Recieved', 'Recieved'), ('Pending', 'Pending')])

class FacultyAttendance(models.Model):
    faculty = models.ForeignKey(faculties, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

class CoursePlanning(models.Model):
    faculty = models.ForeignKey(faculties, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)
    timing = models.TimeField()
    study_plan = models.TextField()