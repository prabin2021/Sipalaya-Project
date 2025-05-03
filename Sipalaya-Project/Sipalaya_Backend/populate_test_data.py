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
from django.core.files.base import ContentFile

# Import all models
from courses.models import Category as CourseCategory, Course, Instructor, Enrollment, DemoClass, DemoClassRegistration, Payment as CoursePayment
from stud_portal.models import Profile, StudentProfile, InstructorProfile, EnrolledCourse, Assignment, Certificate, Attendance, CompletedLesson
from testimonials.models import Testimonial, Review
from demo_classes.models import DemoClass as DemoClassSchedule, DemoClassSchedule as Schedule, DemoClassBooking, DemoClassFeedback
from blog.models import Category as BlogCategory, Blog
from homepage.models import Banner, Feature, Contact
from payments.models import PaymentMethod, Payment, InstallmentPlan

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created")

def create_users():
    # Create instructors
    instructors = [
        ('instructor1', 'instructor1@example.com', 'instructor123', 'Mike', 'Johnson'),
        ('instructor2', 'instructor2@example.com', 'instructor123', 'Sarah', 'Williams')
    ]
    
    instructor_objects = []
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

        # Create Profile
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'instructor',
                'has_completed_profile': True
            }
        )

        # Create InstructorProfile
        instructor_profile, _ = InstructorProfile.objects.get_or_create(
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
        instructor_objects.append(user)  # Append User instead of InstructorProfile
        print(f"Instructor {username} created with profile")

    # Create students
    students = [
        ('student1', 'student1@example.com', 'student123', 'John', 'Doe'),
        ('student2', 'student2@example.com', 'student123', 'Jane', 'Smith')
    ]
    
    student_objects = []
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

        # Create Profile
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'student',
                'has_completed_profile': True
            }
        )

        # Create StudentProfile
        student_profile, _ = StudentProfile.objects.get_or_create(
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
        student_objects.append(user)
        print(f"Student {username} created with profile")

    return instructor_objects, student_objects

def create_course_categories():
    categories = ['Web Development', 'Python Programming', 'Data Science', 'Mobile Development']
    category_objects = []
    
    for cat_name in categories:
        category, created = CourseCategory.objects.get_or_create(
            name=cat_name,
            defaults={
                'description': f'Learn {cat_name} from industry experts'
            }
        )
        if created:
            print(f"Course category {cat_name} created")
        category_objects.append(category)
    
    return category_objects

def create_courses(categories, instructors):
    courses_data = [
        {
            'title': 'Full Stack Web Development',
            'description': 'Learn full stack web development with modern technologies',
            'price': Decimal('45000.00'),
            'duration': 'medium',
            'category': categories[0],  # Web Development
            'instructor': instructors[0],  # Using User instance
            'skill_level': 'intermediate'
        },
        {
            'title': 'Python for Beginners',
            'description': 'Start your programming journey with Python',
            'price': Decimal('25000.00'),
            'duration': 'short',
            'category': categories[1],  # Python Programming
            'instructor': instructors[1],  # Using User instance
            'skill_level': 'beginner'
        }
    ]
    
    course_objects = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        if created:
            print(f"Course {course_data['title']} created")
        course_objects.append(course)
    
    return course_objects

def create_demo_classes(courses):
    for course in courses:
        # Create demo class in demo_classes app
        demo_class = DemoClassSchedule.objects.create(
            course=course,
            title=f'Demo Class for {course.title}',
            description=f'Join our demo class for {course.title}',
            instructor=course.instructor,
            max_participants=10,
            is_active=True
        )
        print(f"Demo class created for {course.title}")

        # Create schedule for the demo class
        schedule = Schedule.objects.create(
            demo_class=demo_class,
            start_time=timezone.now() + timedelta(days=7),
            end_time=timezone.now() + timedelta(days=7, hours=2),
            is_booked=False
        )
        print(f"Demo class schedule created for {course.title}")

        # Create a demo class registration in courses app
        DemoClass.objects.create(
            course=course,
            date=timezone.now() + timedelta(days=7),
            start_time='14:00',
            end_time='16:00',
            instructor=course.instructor,
            max_students=10,
            current_students=0
        )
        print(f"Demo class registration created for {course.title}")

def create_blog_content():
    # Create blog categories
    categories = ['Programming', 'Career', 'Technology']
    author = User.objects.get(username='instructor1')  # Use instructor1 as the author
    
    for i, cat_name in enumerate(categories):
        category, created = BlogCategory.objects.get_or_create(
            name=cat_name,
            description=f'Blog posts about {cat_name.lower()}'
        )
        if created:
            print(f"Blog category {cat_name} created")

        # Create blog posts for each category
        Blog.objects.create(
            title=f'Latest trends in {cat_name}',
            slug=f'latest-trends-in-{cat_name.lower()}-{i}',  # Add index to make slug unique
            content=f'This is a sample blog post about {cat_name.lower()}...',
            category=category,
            author=author,
            is_published=True
        )
        print(f"Blog post created for {cat_name}")

def create_homepage_content():
    # Create banners
    Banner.objects.create(
        title='Welcome to Sipalaya',
        subtitle='Learn from the best instructors',
        image='banners/welcome.jpg',
        is_active=True
    )
    print("Homepage banner created")

    # Create features
    features = ['Expert Instructors', 'Flexible Learning', 'Job Placement']
    for feature_name in features:
        Feature.objects.create(
            title=feature_name,
            description=f'Benefit from our {feature_name.lower()}',
            icon_class='fa-graduation-cap'  # Using Font Awesome icon class
        )
        print(f"Feature {feature_name} created")

def create_payment_methods():
    methods = [
        ('stripe', 'Stripe'),
        ('khalti', 'Khalti')
    ]
    for method_name, display_name in methods:
        PaymentMethod.objects.create(
            name=method_name,
            is_active=True
        )
        print(f"Payment method {display_name} created")

def create_testimonials():
    testimonials = [
        {
            'name': 'John Doe',
            'position': 'Software Developer',
            'company': 'Tech Corp',
            'content': 'Great learning experience!',
            'rating': 5
        },
        {
            'name': 'Jane Smith',
            'position': 'Web Developer',
            'company': 'Web Solutions',
            'content': 'Excellent courses and instructors',
            'rating': 5
        }
    ]
    
    for testimonial_data in testimonials:
        Testimonial.objects.create(**testimonial_data)
        print(f"Testimonial by {testimonial_data['name']} created")

def populate_test_data():
    print("Starting to populate test data...")
    
    # Create users and core data
    create_superuser()
    instructors, students = create_users()
    
    # Create course-related data
    categories = create_course_categories()
    courses = create_courses(categories, instructors)
    create_demo_classes(courses)
    
    # Create content
    create_blog_content()
    create_homepage_content()
    
    # Create payment and testimonial data
    create_payment_methods()
    create_testimonials()
    
    print("Test data population completed!")

if __name__ == '__main__':
    populate_test_data() 