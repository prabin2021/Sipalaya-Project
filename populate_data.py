import os
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sipalaya_Backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from courses.models import Category, Course, Instructor, DemoClass, Payment, DemoClassRegistration, Enrollment
from homepage.models import Banner, Contact, Feature
from stud_portal.models import (EnrolledCourse, CompletedLesson, Certificate, 
                              Attendance, Assignment, InstructorProfile, 
                              Profile, StudentProfile)

def create_users():
    # Create superuser if not exists
    if not User.objects.filter(username='bigyat').exists():
        superuser = User.objects.create_superuser('bigyat', 'tbigyat@gmail.com', 'admin123')
        print("Superuser created")

    # Create students
    students = [
        ('ram', 'ram@example.com', 'ram123', 'Ram', 'Sharma'),
        ('sita', 'sita@example.com', 'sita123', 'Sita', 'Thapa')
    ]
    
    for username, email, password, first_name, last_name in students:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            user.set_password(password)
            user.save()
            StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': f"{first_name} {last_name}",
                    'email': email,
                    'phone': f'98{str(hash(username))[-8:]}',
                    'address': f'{first_name} Street, Kathmandu',
                    'gender': 'M',
                    'has_completed_profile': True
                }
            )
            print(f"Student {username} created")

    # Create instructors
    instructors = [
        ('john', 'john@example.com', 'john123', 'John', 'Doe'),
        ('jane', 'jane@example.com', 'jane123', 'Jane', 'Smith')
    ]
    
    for username, email, password, first_name, last_name in instructors:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            user.set_password(password)
            user.save()
            
            # Create instructor record
            instructor, created = Instructor.objects.get_or_create(
                name=f"{first_name} {last_name}",
                defaults={
                    'bio': f'Experienced instructor specializing in technology education',
                    'experience': 5,
                    'photo': 'instructors/instructor1.jpg'
                }
            )
            if created:
                print(f"Instructor {instructor.name} created")
            
            # Create instructor profile
            InstructorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': f"{first_name} {last_name}",
                    'email': email,
                    'phone': f'98{str(hash(username))[-8:]}',
                    'address': f'{first_name} Avenue, Kathmandu',
                    'gender': 'M',
                    'has_completed_profile': True
                }
            )
            print(f"Instructor profile for {username} created")

def create_categories():
    categories = ['Web Development', 'Python Programming', 'Data Science']
    for cat_name in categories:
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={
                'description': f'Learn {cat_name} from industry experts'
            }
        )
        if created:
            print(f"Category {cat_name} created")

def create_courses():
    web_dev = Category.objects.get(name='Web Development')
    python = Category.objects.get(name='Python Programming')
    data_science = Category.objects.get(name='Data Science')
    
    john = User.objects.get(username='john')
    jane = User.objects.get(username='jane')
    
    courses_data = [
        {
            'title': 'Full Stack Web Development',
            'description': 'Learn full stack web development with modern technologies',
            'price': Decimal('45000.00'),
            'duration': 'medium',
            'category': web_dev,
            'instructor': john,
            'skill_level': 'intermediate',
            'image': 'course_images/course1.jpg',
            'syllabus': """HTML5 & CSS3 Fundamentals
JavaScript ES6+ Programming
React.js Frontend Development
Node.js Backend Development
Database Design with MongoDB
RESTful API Development
Authentication & Authorization
Deployment & DevOps Basics""",
            'prerequisites': """Basic computer knowledge
Understanding of internet concepts
Familiarity with any text editor
Basic problem-solving skills"""
        },
        {
            'title': 'Python for Beginners',
            'description': 'Start your programming journey with Python',
            'price': Decimal('25000.00'),
            'duration': 'short',
            'category': python,
            'instructor': jane,
            'skill_level': 'beginner',
            'image': 'course_images/course1.jpg',
            'syllabus': """Introduction to Python
Variables and Data Types
Control Flow (if, else, loops)
Functions and Modules
Lists, Tuples, and Dictionaries
File Handling
Error Handling
Basic Object-Oriented Programming""",
            'prerequisites': """No prior programming experience required
Basic computer operations
Enthusiasm to learn programming"""
        },
        {
            'title': 'Machine Learning Fundamentals',
            'description': 'Master the basics of machine learning',
            'price': Decimal('65000.00'),
            'duration': 'long',
            'category': data_science,
            'instructor': john,
            'skill_level': 'advanced',
            'image': 'course_images/course1.jpg',
            'syllabus': """Introduction to Machine Learning
Python for Data Science
Data Preprocessing
Supervised Learning
Unsupervised Learning
Neural Networks Basics
Model Evaluation
Deployment of ML Models""",
            'prerequisites': """Python programming knowledge
Basic statistics and probability
Linear algebra fundamentals
Calculus basics"""
        }
    ]
    
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        if created:
            print(f"Course {course_data['title']} created")

def create_demo_classes():
    courses = Course.objects.all()
    for i, course in enumerate(courses):
        demo_date = timezone.now() + timedelta(days=(i+1)*7)
        demo_class, created = DemoClass.objects.get_or_create(
            course=course,
            date=demo_date,
            defaults={
                'start_time': '14:00',
                'end_time': '16:00',
                'instructor': course.instructor,
                'max_students': 10,
                'current_students': 0
            }
        )
        if created:
            print(f"Demo class for {course.title} created")

def create_enrollments_and_payments():
    ram = User.objects.get(username='ram')
    sita = User.objects.get(username='sita')
    
    web_dev = Course.objects.get(title='Full Stack Web Development')
    python = Course.objects.get(title='Python for Beginners')
    
    # Create enrollments
    enrollments = [
        (ram, web_dev, 30),
        (sita, python, 60)
    ]
    
    for student, course, progress in enrollments:
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'enrolled_at': timezone.now(),
                'progress': progress,
                'is_completed': False
            }
        )
        if created:
            print(f"Enrollment created for {student.username} in {course.title}")
        
        # Create payment
        payment, created = Payment.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'amount': course.price,
                'payment_date': timezone.now(),
                'payment_method': 'eSewa' if student == ram else 'Khalti',
                'status': 'Completed'
            }
        )
        if created:
            print(f"Payment created for {student.username}")
        
        # Create enrolled course in student portal
        enrolled_course, created = EnrolledCourse.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'progress': float(progress)
            }
        )
        if created:
            print(f"Enrolled course created for {student.username}")

def create_demo_registrations():
    ram = User.objects.get(username='ram')
    sita = User.objects.get(username='sita')
    
    demo_classes = DemoClass.objects.all()
    
    # Register Ram for Web Development demo
    reg1, created = DemoClassRegistration.objects.get_or_create(
        student=ram,
        demo_class=demo_classes[0]
    )
    if created:
        print(f"Demo registration created for {ram.username}")
    
    # Register Sita for Python demo
    reg2, created = DemoClassRegistration.objects.get_or_create(
        student=sita,
        demo_class=demo_classes[1]
    )
    if created:
        print(f"Demo registration created for {sita.username}")

def create_homepage_content():
    # Create banners
    banner_data = [
        {
            'title': 'Welcome to Sipalaya',
            'description': 'Your gateway to quality IT education',
            'image': 'banners/banner1.jpg'
        },
        {
            'title': 'Learn from Industry Experts',
            'description': 'Get trained by experienced professionals',
            'image': 'banners/banner1.jpg'
        }
    ]
    
    for data in banner_data:
        banner, created = Banner.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        
    # Create features
    feature_data = [
        {
            'title': 'Live Classes',
            'description': 'Interactive live sessions with instructors',
            'icon_class': 'fas fa-video'
        },
        {
            'title': 'Project Based',
            'description': 'Learn by building real projects',
            'icon_class': 'fas fa-project-diagram'
        },
        {
            'title': '24/7 Support',
            'description': 'Round the clock learning support',
            'icon_class': 'fas fa-headset'
        }
    ]
    
    for data in feature_data:
        feature, created = Feature.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        print(f"Feature {data['title']} created")
        
    # Create contact messages
    contact_data = [
        {
            'name': 'John Smith',
            'email': 'john@example.com',
            'phone_number': '+1234567890',
            'message': 'Interested in the Python course'
        },
        {
            'name': 'Mary Johnson',
            'email': 'mary@example.com',
            'phone_number': '+9876543210',
            'message': 'Would like to know more about web development'
        }
    ]
    
    for data in contact_data:
        contact, created = Contact.objects.get_or_create(
            email=data['email'],
            defaults=data
        )
        print(f"Contact message from {data['name']} created")

def create_student_portal_content():
    # Create assignments
    students = User.objects.filter(username__in=['ram', 'sita'])
    courses = Course.objects.all()
    
    # Create enrolled courses
    for student in students:
        # Enroll each student in 1-3 random courses
        num_courses = random.randint(1, 3)
        for _ in range(num_courses):
            course = random.choice(courses)
            progress = random.uniform(0, 100)
            EnrolledCourse.objects.create(
                student=student,
                course=course,
                progress=progress
            )
    
    # Create assignments for enrolled courses
    enrolled_courses = EnrolledCourse.objects.all()
    for enrolled_course in enrolled_courses:
        assignment, created = Assignment.objects.get_or_create(
            student=enrolled_course.student,
            course=enrolled_course,
            defaults={
                'file': f'assignments/assignment_{enrolled_course.course.title.lower().replace(" ", "_")}.pdf',
                'grade': 'A' if enrolled_course.progress > 80 else 'B',
                'feedback': 'Great work!' if enrolled_course.progress > 80 else 'Good effort, keep practicing!'
            }
        )
        if created:
            print(f"Assignment created for {enrolled_course.student.username} in {enrolled_course.course.title}")
    
    # Create attendance records
    for enrolled_course in enrolled_courses:
        attendance, created = Attendance.objects.get_or_create(
            student=enrolled_course.student,
            course=enrolled_course,
            date=timezone.now().date(),
            defaults={'status': True}
        )
        if created:
            print(f"Attendance record created for {enrolled_course.student.username}")
    
    # Create certificates for completed courses
    for enrolled_course in enrolled_courses.filter(progress=100):
        certificate, created = Certificate.objects.get_or_create(
            student=enrolled_course.student,
            course=enrolled_course,
            defaults={
                'certificate_file': f'certificates/cert_{enrolled_course.course.title.lower().replace(" ", "_")}.pdf'
            }
        )
        if created:
            print(f"Certificate created for {enrolled_course.student.username}")
    
    # Create completed lessons
    for enrolled_course in enrolled_courses:
        lesson, created = CompletedLesson.objects.get_or_create(
            student=enrolled_course.student,
            enrolled_course=enrolled_course,
            lesson_id=random.randint(1, 10)
        )
        if created:
            print(f"Completed lesson recorded for {enrolled_course.student.username}")

def populate_data():
    print("\nStarting database population...")
    
    create_users()
    create_categories()
    create_courses()
    create_demo_classes()
    create_enrollments_and_payments()
    create_demo_registrations()
    create_homepage_content()
    create_student_portal_content()
    
    print("\nDatabase population completed successfully!")

if __name__ == '__main__':
    populate_data() 