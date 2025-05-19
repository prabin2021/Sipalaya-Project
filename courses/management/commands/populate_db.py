import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from courses.models import (
    Category, Course, Module, Lesson, Assignment,
    DemoClass, DemoClassBooking, Payment, Invoice,
    Enrollment, LessonProgress, Certificate, Review
)
from instructor.models import InstructorProfile, Resource
from feedback.models import Testimonial

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create superuser
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Created superuser')

        # Create regular user
        if not User.objects.filter(email='user@example.com').exists():
            User.objects.create_user(
                email='user@example.com',
                password='user123',
                first_name='Regular',
                last_name='User'
            )
            self.stdout.write('Created regular user')

        # Create instructor
        if not User.objects.filter(email='instructor@example.com').exists():
            instructor = User.objects.create_user(
                email='instructor@example.com',
                password='instructor123',
                first_name='John',
                last_name='Doe'
            )
            InstructorProfile.objects.create(
                user=instructor,
                bio='Experienced instructor with 10+ years of teaching experience',
                experience='10+ years',
                expertise='Web Development, Python, Django',
                education='MSc in Computer Science',
                achievements='Multiple teaching awards'
            )
            self.stdout.write('Created instructor')

        # Create categories
        categories = [
            {
                'name': 'Web Development',
                'description': 'Learn modern web development technologies',
                'icon': 'fas fa-code'
            },
            {
                'name': 'Data Science',
                'description': 'Master data analysis and machine learning',
                'icon': 'fas fa-chart-bar'
            },
            {
                'name': 'Mobile Development',
                'description': 'Build mobile apps for iOS and Android',
                'icon': 'fas fa-mobile-alt'
            }
        ]

        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
        self.stdout.write('Created categories')

        # Create courses
        instructor = User.objects.get(email='instructor@example.com')
        web_dev = Category.objects.get(name='Web Development')
        data_science = Category.objects.get(name='Data Science')

        courses = [
            {
                'title': 'Complete Web Development Bootcamp',
                'description': 'Learn HTML, CSS, JavaScript, and more',
                'category': web_dev,
                'price': 99.99,
                'level': 'beginner',
                'duration': '3 months',
                'thumbnail': 'https://source.unsplash.com/random/800x600/?coding'
            },
            {
                'title': 'Data Science with Python',
                'description': 'Master data analysis and visualization',
                'category': data_science,
                'price': 149.99,
                'level': 'intermediate',
                'duration': '4 months',
                'thumbnail': 'https://source.unsplash.com/random/800x600/?data'
            }
        ]

        for course_data in courses:
            # Download and save thumbnail
            response = requests.get(course_data['thumbnail'])
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()

            course = Course.objects.create(
                title=course_data['title'],
                description=course_data['description'],
                category=course_data['category'],
                instructor=instructor,
                price=course_data['price'],
                level=course_data['level'],
                duration=course_data['duration']
            )
            course.thumbnail.save(f"{course.slug}.jpg", File(img_temp), save=True)

            # Create modules
            modules = [
                {
                    'title': 'Introduction',
                    'description': 'Get started with the basics'
                },
                {
                    'title': 'Advanced Topics',
                    'description': 'Dive deep into advanced concepts'
                }
            ]

            for module_data in modules:
                module = Module.objects.create(
                    course=course,
                    title=module_data['title'],
                    description=module_data['description']
                )

                # Create lessons
                lessons = [
                    {
                        'title': 'Getting Started',
                        'content': 'Learn the fundamentals',
                        'duration': '1 hour'
                    },
                    {
                        'title': 'Hands-on Practice',
                        'content': 'Apply what you learned',
                        'duration': '2 hours'
                    }
                ]

                for lesson_data in lessons:
                    lesson = Lesson.objects.create(
                        module=module,
                        title=lesson_data['title'],
                        content=lesson_data['content'],
                        duration=lesson_data['duration']
                    )

                    # Create resources
                    resources = [
                        {
                            'title': 'Course Material',
                            'file_type': 'pdf',
                            'file_url': 'https://example.com/material.pdf'
                        },
                        {
                            'title': 'Code Examples',
                            'file_type': 'zip',
                            'file_url': 'https://example.com/code.zip'
                        }
                    ]

                    for resource_data in resources:
                        Resource.objects.create(
                            lesson=lesson,
                            title=resource_data['title'],
                            file_type=resource_data['file_type'],
                            file_url=resource_data['file_url']
                        )

                    # Create assignments
                    Assignment.objects.create(
                        lesson=lesson,
                        title=f'Assignment for {lesson.title}',
                        description='Complete the following tasks',
                        due_date='2025-12-31'
                    )

        self.stdout.write('Created courses with modules, lessons, resources, and assignments')

        # Create demo classes
        for course in Course.objects.all():
            DemoClass.objects.create(
                course=course,
                date='2025-06-01',
                start_time='10:00',
                end_time='12:00',
                max_participants=20,
                is_active=True
            )
        self.stdout.write('Created demo classes')

        # Create enrollments and progress
        user = User.objects.get(email='user@example.com')
        for course in Course.objects.all():
            enrollment = Enrollment.objects.create(
                student=user,
                course=course,
                enrolled_at='2025-01-01'
            )

            # Create lesson progress
            for lesson in Lesson.objects.filter(module__course=course):
                LessonProgress.objects.create(
                    student=user,
                    lesson=lesson,
                    completed=True,
                    completed_at='2025-01-02'
                )

            # Create certificate
            Certificate.objects.create(
                student=user,
                course=course,
                certificate_number=f'CERT-{course.id}-{user.id}',
                issued_at='2025-01-03'
            )

            # Create review
            Review.objects.create(
                student=user,
                course=course,
                rating=5,
                content='Great course! Learned a lot.'
            )

        self.stdout.write('Created enrollments, progress, certificates, and reviews')

        # Create testimonials
        testimonials = [
            {
                'content': 'This platform changed my career!',
                'video_url': 'https://example.com/testimonial1.mp4',
                'is_video': True
            },
            {
                'content': 'Best learning experience ever!',
                'video_url': None,
                'is_video': False
            }
        ]

        for testimonial_data in testimonials:
            Testimonial.objects.create(
                student=user,
                content=testimonial_data['content'],
                video_url=testimonial_data['video_url'],
                is_video=testimonial_data['is_video'],
                is_approved=True
            )

        self.stdout.write('Created testimonials')
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data')) 