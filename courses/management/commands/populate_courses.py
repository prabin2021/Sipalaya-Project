from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course, Module, Lesson
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample courses and related data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            {
                'name': 'Web Development',
                'slug': 'web-development',
                'description': 'Learn modern web development technologies and frameworks',
                'icon': 'fas fa-code'
            },
            {
                'name': 'Mobile Development',
                'slug': 'mobile-development',
                'description': 'Master mobile app development for iOS and Android',
                'icon': 'fas fa-mobile-alt'
            },
            {
                'name': 'Data Science',
                'slug': 'data-science',
                'description': 'Learn data analysis, machine learning, and AI',
                'icon': 'fas fa-chart-bar'
            },
            {
                'name': 'Digital Marketing',
                'slug': 'digital-marketing',
                'description': 'Master digital marketing strategies and tools',
                'icon': 'fas fa-bullhorn'
            }
        ]

        for cat_data in categories:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )

        # Create an instructor if not exists
        instructor, created = User.objects.get_or_create(
            email='instructor@sipalaya.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'is_staff': True
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()

        # Sample courses data
        courses_data = [
            {
                'title': 'Complete Web Development Bootcamp',
                'slug': 'web-development-bootcamp',
                'description': 'Master web development from scratch. Learn HTML, CSS, JavaScript, React, Node.js, and more.',
                'category': 'web-development',
                'level': 'beginner',
                'duration': 'long',
                'duration_weeks': 12,
                'price': 999.99,
                'prerequisites': 'Basic computer knowledge',
                'is_featured': True
            },
            {
                'title': 'Flutter Mobile App Development',
                'slug': 'flutter-mobile-development',
                'description': 'Build beautiful, natively compiled applications for mobile, web, and desktop from a single codebase.',
                'category': 'mobile-development',
                'level': 'intermediate',
                'duration': 'medium',
                'duration_weeks': 8,
                'price': 799.99,
                'prerequisites': 'Basic programming knowledge',
                'is_featured': True
            },
            {
                'title': 'Python for Data Science',
                'slug': 'python-data-science',
                'description': 'Learn Python programming for data analysis, visualization, and machine learning.',
                'category': 'data-science',
                'level': 'beginner',
                'duration': 'medium',
                'duration_weeks': 6,
                'price': 699.99,
                'prerequisites': 'Basic mathematics',
                'is_featured': False
            },
            {
                'title': 'Digital Marketing Masterclass',
                'slug': 'digital-marketing-masterclass',
                'description': 'Comprehensive course covering SEO, SEM, Social Media Marketing, and Content Marketing.',
                'category': 'digital-marketing',
                'level': 'beginner',
                'duration': 'short',
                'duration_weeks': 4,
                'price': 499.99,
                'prerequisites': 'None',
                'is_featured': True
            }
        ]

        # Create courses and their modules
        for course_data in courses_data:
            category = Category.objects.get(slug=course_data['category'])
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults={
                    'title': course_data['title'],
                    'description': course_data['description'],
                    'category': category,
                    'instructor': instructor,
                    'level': course_data['level'],
                    'duration': course_data['duration'],
                    'duration_weeks': course_data['duration_weeks'],
                    'price': course_data['price'],
                    'prerequisites': course_data['prerequisites'],
                    'is_featured': course_data['is_featured'],
                    'enrollment_deadline': timezone.now() + timedelta(days=30)
                }
            )

            if created:
                # Create modules for each course
                modules_data = [
                    {
                        'title': 'Introduction',
                        'description': 'Course overview and setup',
                        'order': 1,
                        'lessons': [
                            {
                                'title': 'Welcome to the Course',
                                'content': 'Introduction to the course and what you will learn.',
                                'order': 1
                            },
                            {
                                'title': 'Course Setup',
                                'content': 'Setting up your development environment.',
                                'order': 2
                            }
                        ]
                    },
                    {
                        'title': 'Fundamentals',
                        'description': 'Core concepts and basics',
                        'order': 2,
                        'lessons': [
                            {
                                'title': 'Basic Concepts',
                                'content': 'Understanding the fundamental concepts.',
                                'order': 1
                            },
                            {
                                'title': 'Hands-on Practice',
                                'content': 'Practical exercises to reinforce learning.',
                                'order': 2
                            }
                        ]
                    }
                ]

                for module_data in modules_data:
                    module = Module.objects.create(
                        course=course,
                        title=module_data['title'],
                        description=module_data['description'],
                        order=module_data['order']
                    )

                    for lesson_data in module_data['lessons']:
                        Lesson.objects.create(
                            module=module,
                            title=lesson_data['title'],
                            content=lesson_data['content'],
                            order=lesson_data['order']
                        )

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created course "{course.title}" with modules and lessons')
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated courses data')) 