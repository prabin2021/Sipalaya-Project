import os
import requests
import tempfile
from PIL import Image
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
from courses.models import (
    Course, Module, Lesson, Category, Enrollment, Payment, LessonProgress,
    Assignment, Submission, DemoClass, DemoClassBooking, Certificate, Review
)
from blog.models import Category as BlogCategory, BlogPost, Comment, Tag
from careers.models import JobListing, CompanyPartnership
from feedback.models import Testimonial
from instructor.models import InstructorProfile, Resource
import random
from datetime import timedelta
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def download_and_save_image(self, url, save_path):
        """Downloads an image from URL and saves it to the specified path."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_temp = tempfile.NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                # Open the image to verify it and potentially resize
                image = Image.open(img_temp.name)
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                
                # Save the processed image
                image.save(img_temp.name, 'JPEG')
                return img_temp
            return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to download image: {str(e)}'))
            return None

    def create_pdf_resource(self, title, content, save_path):
        """Creates a PDF file with the given content."""
        try:
            import fpdf
            pdf = fpdf.FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=title, ln=1, align='C')
            pdf.multi_cell(0, 10, txt=content)
            
            temp_pdf = tempfile.NamedTemporaryFile(delete=True, suffix='.pdf')
            pdf.output(temp_pdf.name)
            return temp_pdf
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to create PDF: {str(e)}'))
            return None

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        # Sample image URLs for courses
        course_images = [
            'https://images.unsplash.com/photo-1526379095098-d400fd0bf935',  # Python
            'https://images.unsplash.com/photo-1547658719-da2b51169166',  # Django
            'https://images.unsplash.com/photo-1485796826113-174aa68fd81b',  # Machine Learning
        ]
        
        # Sample image URLs for blog posts
        blog_images = [
            'https://images.unsplash.com/photo-1515879218367-8466d910aaa4',  # Tech
            'https://images.unsplash.com/photo-1461749280684-dccba630e2f6',  # Coding
            'https://images.unsplash.com/photo-1504639725590-34d0984388bd',  # Career
        ]
        
        # Sample image URLs for instructors
        instructor_images = [
            'https://images.unsplash.com/photo-1568602471122-7832951cc4c5',  # Male 1
            'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2',  # Female 1
            'https://images.unsplash.com/photo-1560250097-0b93528c311a',  # Male 2
        ]

        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user')

        # Create regular users if they don't exist
        users = []
        for i in range(5):
            email = f'user{i}@example.com'
            username = f'user{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': 'password123',
                    'first_name': f'User {i}',
                    'last_name': 'Test'
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.email}')
            else:
                self.stdout.write(f'User already exists: {user.email}')

        # Create instructors if they don't exist
        instructors = []
        for i in range(3):
            email = f'instructor{i}@example.com'
            username = f'instructor{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': 'password123',
                    'first_name': f'Instructor {i}',
                    'last_name': 'Smith'
                }
            )
            
            # Download and save instructor profile image
            img_temp = self.download_and_save_image(instructor_images[i], f'instructors/profiles/instructor_{i}.jpg')
            
            instructor, created = InstructorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Experienced instructor in technology and programming. Specializing in Python, Django, and web development.',
                    'experience': '5+ years of teaching experience',
                    'certifications': 'AWS Certified Developer, Microsoft Certified Trainer'
                }
            )
            
            if img_temp:
                instructor.profile_photo.save(f'instructor_{i}.jpg', File(img_temp))
                img_temp.close()
            
            instructors.append(instructor)
            if created:
                self.stdout.write(f'Created instructor: {instructor.user.email}')
            else:
                self.stdout.write(f'Instructor already exists: {instructor.user.email}')

        # Create course categories
        categories = []
        category_names = [
            ('Web Development', 'fa-code'),
            ('Mobile Development', 'fa-mobile-alt'),
            ('Data Science', 'fa-chart-bar'),
            ('Machine Learning', 'fa-brain'),
            ('Cloud Computing', 'fa-cloud')
        ]
        for name, icon in category_names:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'Learn everything about {name}',
                    'slug': slugify(name),
                    'icon': icon
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Create blog categories and tags
        blog_categories = []
        blog_category_names = ['Technology', 'Programming', 'Career Tips', 'Industry News', 'Tutorials']
        for name in blog_category_names:
            category, created = BlogCategory.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            blog_categories.append(category)
            if created:
                self.stdout.write(f'Created blog category: {category.name}')
            else:
                self.stdout.write(f'Blog category already exists: {category.name}')

        # Create blog tags
        tags = []
        tag_names = ['Python', 'Django', 'JavaScript', 'React', 'Machine Learning', 'AI', 'Web Development', 'Mobile Development']
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
            else:
                self.stdout.write(f'Tag already exists: {tag.name}')

        # Create courses
        courses = []
        course_data = [
            {
                'title': 'Complete Python Bootcamp',
                'description': 'Learn Python from scratch to advanced level',
                'price': 99.99,
                'duration': 'medium',
                'duration_weeks': 8,
                'level': 'beginner',
                'prerequisites': 'Basic computer knowledge',
                'syllabus': '''
                Module 1: Python Basics
                - Variables and Data Types
                - Control Flow
                - Functions and Modules
                
                Module 2: Object-Oriented Programming
                - Classes and Objects
                - Inheritance
                - Polymorphism
                
                Module 3: Advanced Python
                - Decorators
                - Generators
                - Context Managers
                ''',
                'youtube_url': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc',
                'image_url': course_images[0]
            },
            {
                'title': 'Django Web Development',
                'description': 'Build web applications with Django',
                'price': 149.99,
                'duration': 'medium',
                'duration_weeks': 10,
                'level': 'intermediate',
                'prerequisites': 'Basic Python knowledge',
                'syllabus': '''
                Module 1: Django Basics
                - MVT Architecture
                - URL Routing
                - Views and Templates
                
                Module 2: Models and Database
                - Model Design
                - Migrations
                - QuerySets
                
                Module 3: Advanced Django
                - Forms and Authentication
                - REST APIs
                - Deployment
                ''',
                'youtube_url': 'https://www.youtube.com/watch?v=F5mRW0jo-U4',
                'image_url': course_images[1]
            },
            {
                'title': 'Machine Learning Fundamentals',
                'description': 'Introduction to machine learning concepts and algorithms',
                'price': 199.99,
                'duration': 'long',
                'duration_weeks': 12,
                'level': 'advanced',
                'prerequisites': 'Python, Basic Statistics',
                'syllabus': '''
                Module 1: ML Basics
                - Data Preprocessing
                - Feature Engineering
                - Model Evaluation
                
                Module 2: Supervised Learning
                - Linear Regression
                - Classification
                - Decision Trees
                
                Module 3: Advanced Topics
                - Neural Networks
                - Deep Learning
                - Model Deployment
                ''',
                'youtube_url': 'https://www.youtube.com/watch?v=KNAWp2S3w94',
                'image_url': course_images[2]
            }
        ]

        for idx, data in enumerate(course_data):
            course, created = Course.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'duration': data['duration'],
                    'duration_weeks': data['duration_weeks'],
                    'level': data['level'],
                    'prerequisites': data['prerequisites'],
                    'syllabus': data['syllabus'],
                    'slug': slugify(data['title']),
                    'instructor': random.choice(instructors).user,
                    'category': random.choice(categories),
                    'enrollment_deadline': timezone.now() + timedelta(days=30),
                    'is_featured': random.choice([True, False]),
                    'demo_class_available': True
                }
            )
            
            # Download and save course image
            if created:
                img_temp = self.download_and_save_image(data['image_url'], f'courses/thumbnails/course_{idx}.jpg')
                if img_temp:
                    course.image.save(f'course_{idx}.jpg', File(img_temp))
                    img_temp.close()
            
            courses.append(course)
            if created:
                self.stdout.write(f'Created course: {course.title}')
            else:
                self.stdout.write(f'Course already exists: {course.title}')

            # Create modules and lessons for each course
            for i in range(3):
                module, created = Module.objects.get_or_create(
                    course=course,
                    title=f'Module {i+1}',
                    defaults={
                        'description': f'Description for module {i+1}',
                        'order': i+1
                    }
                )
                
                for j in range(4):
                    lesson, created = Lesson.objects.get_or_create(
                        module=module,
                        title=f'Lesson {j+1}',
                        defaults={
                            'content': f'Content for lesson {j+1}',
                            'order': j+1,
                            'video_url': f'https://www.youtube.com/watch?v=video{j+1}'
                        }
                    )
                    if created:
                        self.stdout.write(f'Created lesson: {lesson.title} for {course.title}')

                        # Create PDF resource for the lesson
                        pdf_temp = self.create_pdf_resource(
                            f'{lesson.title} - Study Material',
                            f'This is the study material for {lesson.title} of {module.title} in {course.title}.',
                            f'courses/resources/lesson_{lesson.id}_material.pdf'
                        )
                        if pdf_temp:
                            resource = Resource.objects.create(
                                title=f'{lesson.title} - Study Material',
                                description=f'Study material for {lesson.title}',
                                resource_type='document',
                                lesson=lesson
                            )
                            resource.file.save(f'lesson_{lesson.id}_material.pdf', File(pdf_temp))
                            pdf_temp.close()

                    # Create assignments for some lessons
                    if random.choice([True, False]):
                        assignment, created = Assignment.objects.get_or_create(
                            lesson=lesson,
                            title=f'Assignment {j+1}',
                            defaults={
                                'description': f'Complete this assignment to test your understanding of {lesson.title}',
                                'due_date': timezone.now() + timedelta(days=7)
                            }
                        )
                        if created:
                            self.stdout.write(f'Created assignment: {assignment.title}')

        # Create blog posts
        for i in range(10):
            post, created = BlogPost.objects.get_or_create(
                title=f'Blog Post {i+1}',
                defaults={
                    'content': f'This is the content of blog post {i+1}. It contains detailed information about various topics.',
                    'author': random.choice(instructors).user,
                    'category': random.choice(blog_categories),
                    'slug': slugify(f'blog-post-{i+1}'),
                    'status': 'published',
                    'excerpt': f'This is a brief excerpt from blog post {i+1}.',
                    'meta_description': f'Meta description for blog post {i+1}',
                    'meta_keywords': 'python, django, web development',
                    'published_at': timezone.now()
                }
            )
            
            if created:
                # Add featured image to blog post
                img_temp = self.download_and_save_image(
                    random.choice(blog_images),
                    f'blog/images/post_{i+1}.jpg'
                )
                if img_temp:
                    post.featured_image.save(f'post_{i+1}.jpg', File(img_temp))
                    img_temp.close()

                # Add random tags to the post
                post.tags.add(*random.sample(tags, k=random.randint(1, 3)))
                self.stdout.write(f'Created blog post: {post.title}')

                # Create comments for each post
                for j in range(3):
                    Comment.objects.create(
                        post=post,
                        author=random.choice(users),
                        content=f'This is comment {j+1} on post {i+1}'
                    )

        # Create company partnerships
        companies = []
        company_names = ['Tech Corp', 'Digital Solutions', 'AI Innovations', 'Web Masters', 'Cloud Tech']
        for name in company_names:
            company, created = CompanyPartnership.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'{name} is a leading technology company.',
                    'website': f'https://www.{slugify(name)}.com'
                }
            )
            companies.append(company)
            if created:
                self.stdout.write(f'Created company: {company.name}')

        # Create job listings
        job_titles = ['Python Developer', 'Django Developer', 'Data Scientist', 'Machine Learning Engineer', 'DevOps Engineer']
        for title in job_titles:
            job, created = JobListing.objects.get_or_create(
                title=title,
                defaults={
                    'company': random.choice(companies),
                    'description': f'We are looking for a {title} to join our team.',
                    'requirements': 'Python, Django, SQL',
                    'location': 'Remote',
                    'salary_range': '$80,000 - $120,000',
                    'job_type': 'full-time',
                    'application_deadline': timezone.now().date() + timedelta(days=30),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created job listing: {job.title}')

        # Create testimonials
        testimonial_texts = [
            'Great learning experience! The courses are well-structured and the instructors are knowledgeable.',
            'I learned a lot from these courses. The practical examples were very helpful.',
            'The platform is user-friendly and the content is up-to-date with industry standards.',
            'Excellent teaching methodology. I would recommend these courses to anyone.',
            'The support team is very responsive and helpful.'
        ]
        
        for text in testimonial_texts:
            testimonial, created = Testimonial.objects.get_or_create(
                student=random.choice(users),
                content=text,
                defaults={'is_approved': True}
            )
            if created:
                self.stdout.write(f'Created testimonial')

        # Create enrollments, progress, and certificates
        for course in courses:
            for user in users:
                if random.choice([True, False]):
                    # Create enrollment
                    enrollment, created = Enrollment.objects.get_or_create(
                        student=user,
                        course=course,
                        defaults={'enrolled_at': timezone.now() - timedelta(days=random.randint(1, 30))}
                    )
                    if created:
                        self.stdout.write(f'Created enrollment for {user.email} in {course.title}')

                        # Create payment for enrollment
                        payment = Payment.objects.create(
                            student=user,
                            course=course,
                            amount=course.price,
                            status='completed',
                            payment_type='full',
                            transaction_id=f"TRX-{uuid.uuid4().hex[:8].upper()}"
                        )
                        enrollment.payment = payment
                        enrollment.save()

                        # Create progress for some lessons
                        for module in course.modules.all():
                            for lesson in module.lessons.all():
                                if random.choice([True, False]):
                                    LessonProgress.objects.create(
                                        student=user,
                                        lesson=lesson,
                                        completed=True,
                                        completed_at=timezone.now()
                                    )

                        # Create certificate if course is completed
                        if random.choice([True, False]):
                            Certificate.objects.create(
                                student=user,
                                course=course,
                                certificate_number=f"CERT-{uuid.uuid4().hex[:8].upper()}"
                            )
                            self.stdout.write(f'Created certificate for {user.email} in {course.title}')

                        # Create review
                        Review.objects.create(
                            student=user,
                            course=course,
                            rating=random.randint(4, 5),
                            comment=f'Great course! Learned a lot about {course.title}.'
                        )

        # Create demo classes
        for course in courses:
            if course.demo_class_available:
                for i in range(2):
                    demo_class = DemoClass.objects.create(
                        course=course,
                        date=timezone.now().date() + timedelta(days=i*7),
                        time=timezone.now().time(),
                        capacity=20
                    )
                    self.stdout.write(f'Created demo class for {course.title}')

                    # Create some bookings
                    for _ in range(random.randint(1, 5)):
                        DemoClassBooking.objects.create(
                            demo_class=demo_class,
                            student=random.choice(users),
                            status=random.choice(['pending', 'confirmed'])
                        )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data')) 