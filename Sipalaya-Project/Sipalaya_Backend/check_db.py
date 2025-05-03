import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sipalaya_Backend.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Category, Course, Instructor, DemoClass, Payment, DemoClassRegistration, Enrollment
from homepage.models import Banner, Contact, Feature
from stud_portal.models import EnrolledCourse, CompletedLesson, Certificate, Attendance, Assignment, InstructorProfile, Profile, StudentProfile

def check_database():
    print("\n=== Checking Database Contents ===\n")
    
    # Check Users
    print("=== Users ===")
    users = User.objects.all()
    print(f"Total Users: {users.count()}")
    for user in users:
        print(f"- {user.username} ({user.email})")
    
    # Check Categories
    print("\n=== Categories ===")
    categories = Category.objects.all()
    print(f"Total Categories: {categories.count()}")
    for category in categories:
        print(f"- {category.name}")
    
    # Check Courses
    print("\n=== Courses ===")
    courses = Course.objects.all()
    print(f"Total Courses: {courses.count()}")
    for course in courses:
        print(f"- {course.title} (Rs. {course.price})")
    
    # Check Instructors
    print("\n=== Instructors ===")
    instructors = Instructor.objects.all()
    print(f"Total Instructors: {instructors.count()}")
    for instructor in instructors:
        print(f"- {instructor.user.username}")
    
    # Check Demo Classes
    print("\n=== Demo Classes ===")
    demo_classes = DemoClass.objects.all()
    print(f"Total Demo Classes: {demo_classes.count()}")
    for demo in demo_classes:
        print(f"- {demo.course.title} on {demo.date}")
    
    # Check Enrollments
    print("\n=== Enrollments ===")
    enrollments = Enrollment.objects.all()
    print(f"Total Enrollments: {enrollments.count()}")
    for enrollment in enrollments:
        print(f"- {enrollment.student.username} in {enrollment.course.title}")
    
    # Check Payments
    print("\n=== Payments ===")
    payments = Payment.objects.all()
    print(f"Total Payments: {payments.count()}")
    for payment in payments:
        print(f"- {payment.student.username} paid Rs. {payment.amount} for {payment.course.title}")
    
    # Check Demo Class Registrations
    print("\n=== Demo Class Registrations ===")
    registrations = DemoClassRegistration.objects.all()
    print(f"Total Registrations: {registrations.count()}")
    for reg in registrations:
        print(f"- {reg.student.username} registered for {reg.demo_class.course.title}")
    
    # Check Homepage Models
    print("\n=== Homepage Models ===")
    banners = Banner.objects.all()
    contacts = Contact.objects.all()
    features = Feature.objects.all()
    print(f"Banners: {banners.count()}")
    print(f"Contacts: {contacts.count()}")
    print(f"Features: {features.count()}")
    
    # Check Student Portal Models
    print("\n=== Student Portal Models ===")
    enrolled_courses = EnrolledCourse.objects.all()
    completed_lessons = CompletedLesson.objects.all()
    certificates = Certificate.objects.all()
    attendance = Attendance.objects.all()
    assignments = Assignment.objects.all()
    instructor_profiles = InstructorProfile.objects.all()
    student_profiles = StudentProfile.objects.all()
    
    print(f"Enrolled Courses: {enrolled_courses.count()}")
    print(f"Completed Lessons: {completed_lessons.count()}")
    print(f"Certificates: {certificates.count()}")
    print(f"Attendance Records: {attendance.count()}")
    print(f"Assignments: {assignments.count()}")
    print(f"Instructor Profiles: {instructor_profiles.count()}")
    print(f"Student Profiles: {student_profiles.count()}")

if __name__ == '__main__':
    check_database() 