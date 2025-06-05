from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files import File
from django.db import transaction
from courses.models import (
    Category, Course, Module, Lesson, Assignment,
    DemoClass, DemoClassBooking, Enrollment, LessonProgress, Review,
    Certificate
)
from instructor.models import InstructorProfile
from core.models import (
    Banner, Testimonial, Statistic, Service,
    CompanyInfo, Milestone, Partnership, TeamMember,
    Certification
)
from blog.models import BlogPost, Category as BlogCategory, Tag
from careers.models import (
    PlacementService, CompanyPartnership,
    JobListing, AlumniSuccessStory
)
from feedback.models import Review as CourseReview
import random
from datetime import timedelta
import os
from django.conf import settings
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')
        
        with transaction.atomic():
            # Create superuser
            if not User.objects.filter(email='admin@sipalaya.com').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@sipalaya.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write('Created superuser')

            # Create regular users
            instructors, students = self.create_users()
            
            # Create categories
            self.create_categories()
            
            # Create courses
            self.create_courses()
            
            # Create blog categories and tags
            self.create_blog_categories()
            self.create_blog_tags()
            
            # Create blog posts
            self.create_blog_posts()
            
            # Create testimonials
            self.create_testimonials()
            
            # Create statistics
            self.create_statistics()
            
            # Create services
            self.create_services()
            
            # Create company info
            self.create_company_info()
            
            # Create placement services
            self.create_placement_services()
            
            # Create job listings
            self.create_job_listings()
            
            # Create alumni success stories
            self.create_alumni_stories()

            # Create team members
            self.create_team_members()

            # Create milestones
            self.create_milestones()

            # Create partnerships and certifications
            self.create_partnerships_and_certifications()

            # Create demo classes and bookings
            self.create_demo_classes_and_bookings(students)

            # Create course reviews
            self.create_course_reviews(students)

            # Create course certificates
            self.create_course_certificates(students)

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))

    def create_users(self):
        # Create instructors
        instructors = []
        for i in range(5):
            instructor, created = User.objects.get_or_create(
                username=f'instructor{i}',
                defaults={
                    'email': f'instructor{i}@sipalaya.com',
                    'password': 'instructor123',
                    'first_name': f'Instructor{i}',
                    'last_name': f'Last{i}'
                }
            )
            if created:
                instructor.set_password('instructor123')
                instructor.save()
                # Create instructor profile
                InstructorProfile.objects.create(
                    user=instructor,
                    bio=f'Experienced instructor specializing in technology education. Has been teaching for {i+5} years.',
                    experience=f'Senior Developer at Tech Company {i+1}\nLead Instructor at Coding Bootcamp\nTechnical Consultant',
                    certifications=f'AWS Certified Solutions Architect\nGoogle Cloud Professional\nMicrosoft Certified Trainer'
                )
                self.stdout.write(f'Created instructor: {instructor.email}')
            else:
                self.stdout.write(f'Instructor already exists: {instructor.email}')
            instructors.append(instructor)

        # Create students
        students = []
        for i in range(20):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@sipalaya.com',
                    'password': 'student123',
                    'first_name': f'Student{i}',
                    'last_name': f'Last{i}'
                }
            )
            if created:
                student.set_password('student123')
                student.save()
                self.stdout.write(f'Created student: {student.email}')
            else:
                self.stdout.write(f'Student already exists: {student.email}')
            students.append(student)

        return instructors, students

    def create_categories(self):
        categories = [
            'Web Development',
            'Mobile Development',
            'Data Science',
            'Digital Marketing',
            'Graphic Design',
            'Network Security',
            'Cloud Computing',
            'Artificial Intelligence'
        ]
        
        created_categories = []
        for category in categories:
            slug = slugify(category)
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': category,
                    'description': f'Learn {category} with our expert instructors'
                }
            )
            created_categories.append(cat)
            if created:
                self.stdout.write(f'Created category: {category}')
            else:
                self.stdout.write(f'Category already exists: {category}')
        
        return created_categories

    def create_blog_categories(self):
        categories = [
            'Technology',
            'Education',
            'Career Development',
            'Industry News',
            'Student Success'
        ]
        
        created_categories = []
        for category in categories:
            slug = slugify(category)
            cat, created = BlogCategory.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': category,
                    'description': f'Articles about {category.lower()}'
                }
            )
            created_categories.append(cat)
            if created:
                self.stdout.write(f'Created blog category: {category}')
            else:
                self.stdout.write(f'Blog category already exists: {category}')
        
        return created_categories

    def create_blog_tags(self):
        tags = [
            'Web Development',
            'Python',
            'Data Science',
            'Career Tips',
            'Learning',
            'Technology',
            'Education',
            'Success Stories'
        ]
        
        created_tags = []
        for tag in tags:
            slug = slugify(tag)
            tag_obj, created = Tag.objects.get_or_create(
                slug=slug,
                defaults={'name': tag}
            )
            created_tags.append(tag_obj)
            if created:
                self.stdout.write(f'Created blog tag: {tag}')
            else:
                self.stdout.write(f'Blog tag already exists: {tag}')
        
        return created_tags

    def create_courses(self):
        instructors = User.objects.filter(instructor_profile__isnull=False)
        categories = Category.objects.all()
        
        course_data = [
            {
                'title': 'Complete Web Development Bootcamp',
                'description': 'Learn HTML, CSS, JavaScript, and more',
                'price': 15000,
                'duration': '3 months',
                'level': 'beginner'
            },
            {
                'title': 'Python for Data Science',
                'description': 'Master Python programming for data analysis',
                'price': 20000,
                'duration': '4 months',
                'level': 'intermediate'
            },
            {
                'title': 'Mobile App Development with Flutter',
                'description': 'Build cross-platform mobile apps',
                'price': 25000,
                'duration': '3 months',
                'level': 'advanced'
            }
        ]
        
        for data in course_data:
            slug = slugify(data['title'])
            course, created = Course.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'price': data['price'],
                    'duration': data['duration'],
                    'level': data['level'],
                    'instructor': random.choice(instructors),
                    'category': random.choice(categories)
                }
            )
            
            if created:
                # Create modules
                for i in range(3):
                    module = Module.objects.create(
                        course=course,
                        title=f'Module {i+1}',
                        description=f'Description for module {i+1}',
                        order=i+1
                    )
                    
                    # Create lessons
                    for j in range(5):
                        lesson = Lesson.objects.create(
                            module=module,
                            title=f'Lesson {j+1}',
                            content=f'Content for lesson {j+1}',
                            order=j+1
                        )
                        
                        # Create assignment
                        Assignment.objects.create(
                            lesson=lesson,
                            title=f'Assignment {j+1}',
                            description=f'Description for assignment {j+1}',
                            due_date=timezone.now() + timedelta(days=7)
                        )
                
                self.stdout.write(f'Created course: {course.title}')
            else:
                self.stdout.write(f'Course already exists: {course.title}')

    def create_blog_posts(self):
        categories = BlogCategory.objects.all()
        tags = Tag.objects.all()
        authors = User.objects.filter(instructor_profile__isnull=False)
        
        blog_data = [
            {
                'title': 'Getting Started with Web Development',
                'content': 'Learn the basics of web development...',
                'excerpt': 'A beginner\'s guide to web development'
            },
            {
                'title': 'The Future of AI in Education',
                'content': 'Exploring how AI is transforming education...',
                'excerpt': 'AI\'s impact on modern education'
            },
            {
                'title': 'Career Opportunities in Tech',
                'content': 'Discover various career paths in technology...',
                'excerpt': 'Exploring tech career options'
            }
        ]
        
        for data in blog_data:
            slug = slugify(data['title'])
            post, created = BlogPost.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': data['title'],
                    'content': data['content'],
                    'excerpt': data['excerpt'],
                    'author': random.choice(authors),
                    'category': random.choice(categories),
                    'status': 'published'
                }
            )
            if created:
                post.tags.add(*random.sample(list(tags), 2))
                self.stdout.write(f'Created blog post: {post.title}')
            else:
                self.stdout.write(f'Blog post already exists: {post.title}')

    def create_testimonials(self):
        students = User.objects.filter(instructor_profile__isnull=True)
        
        testimonial_data = [
            {
                'name': 'John Doe',
                'position': 'Software Developer',
                'company': 'Tech Solutions',
                'content': 'The courses at Sipalaya Info Tech helped me launch my career in tech!'
            },
            {
                'name': 'Jane Smith',
                'position': 'Data Analyst',
                'company': 'Data Insights',
                'content': 'Excellent instructors and comprehensive curriculum.'
            }
        ]
        
        for data in testimonial_data:
            Testimonial.objects.create(
                name=data['name'],
                position=data['position'],
                company=data['company'],
                content=data['content'],
                rating=random.randint(4, 5)
            )
            self.stdout.write(f'Created testimonial for: {data["name"]}')

    def create_statistics(self):
        statistics_data = [
            {
                'title': 'Students Trained',
                'value': 5000,
                'icon': 'fas fa-users'
            },
            {
                'title': 'Courses Offered',
                'value': 50,
                'icon': 'fas fa-book'
            },
            {
                'title': 'Success Rate',
                'value': 95,
                'icon': 'fas fa-chart-line'
            },
            {
                'title': 'Expert Instructors',
                'value': 20,
                'icon': 'fas fa-chalkboard-teacher'
            }
        ]
        
        for data in statistics_data:
            Statistic.objects.create(**data)
            self.stdout.write(f'Created statistic: {data["title"]}')

    def create_services(self):
        services_data = [
            {
                'title': 'IT Training',
                'description': 'Comprehensive IT training programs',
                'icon': 'fas fa-laptop-code'
            },
            {
                'title': 'Career Guidance',
                'description': 'Expert career counseling and placement support',
                'icon': 'fas fa-briefcase'
            },
            {
                'title': 'Certification',
                'description': 'Industry-recognized certifications',
                'icon': 'fas fa-certificate'
            }
        ]
        
        for data in services_data:
            Service.objects.create(**data)
            self.stdout.write(f'Created service: {data["title"]}')

    def create_company_info(self):
        CompanyInfo.objects.create(
            mission='To provide quality IT education and create skilled professionals',
            vision='To be the leading IT education provider in Nepal',
            history='Sipalaya Info Tech was founded with the goal of bridging the gap between academia and industry requirements...',
            established_date=timezone.now().date()
        )
        self.stdout.write('Created company info')

    def create_placement_services(self):
        services_data = [
            {
                'title': 'Resume Building',
                'description': 'Professional resume writing and optimization',
                'icon': 'fas fa-file-alt'
            },
            {
                'title': 'Interview Preparation',
                'description': 'Mock interviews and interview skills training',
                'icon': 'fas fa-comments'
            },
            {
                'title': 'Job Placement',
                'description': 'Direct placement in partner companies',
                'icon': 'fas fa-handshake'
            }
        ]
        
        for data in services_data:
            PlacementService.objects.create(**data)
            self.stdout.write(f'Created placement service: {data["title"]}')

    def create_job_listings(self):
        # Create company partnerships first
        companies = [
            {
                'name': 'Tech Solutions',
                'description': 'Leading software development company',
                'website': 'https://techsolutions.com'
            },
            {
                'name': 'Data Insights',
                'description': 'Data analytics and consulting firm',
                'website': 'https://datainsights.com'
            }
        ]
        
        created_companies = []
        for data in companies:
            company, created = CompanyPartnership.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'website': data['website']
                }
            )
            created_companies.append(company)
            if created:
                self.stdout.write(f'Created company partnership: {company.name}')
            else:
                self.stdout.write(f'Company partnership already exists: {company.name}')

        # Create job listings
        job_data = [
            {
                'title': 'Junior Web Developer',
                'company': created_companies[0],
                'description': 'Looking for a junior web developer...',
                'requirements': 'HTML, CSS, JavaScript',
                'location': 'Kathmandu',
                'job_type': 'full-time',
                'salary_range': '30,000 - 40,000'
            },
            {
                'title': 'Data Analyst',
                'company': created_companies[1],
                'description': 'Seeking a data analyst...',
                'requirements': 'Python, SQL, Data Analysis',
                'location': 'Kathmandu',
                'job_type': 'full-time',
                'salary_range': '40,000 - 50,000'
            }
        ]
        
        for data in job_data:
            job, created = JobListing.objects.get_or_create(
                title=data['title'],
                company=data['company'],
                defaults={
                    'description': data['description'],
                    'requirements': data['requirements'],
                    'location': data['location'],
                    'job_type': data['job_type'],
                    'salary_range': data['salary_range'],
                    'application_deadline': timezone.now().date() + timedelta(days=30)
                }
            )
            if created:
                self.stdout.write(f'Created job listing: {job.title}')
            else:
                self.stdout.write(f'Job listing already exists: {job.title}')

    def create_alumni_stories(self):
        stories_data = [
            {
                'name': 'Ram Sharma',
                'graduation_year': 2023,
                'current_position': 'Senior Developer',
                'company': 'Tech Solutions',
                'story': 'Started as a student at Sipalaya Info Tech and transformed my career through intensive training. Now working as a Senior Developer, leading projects and mentoring junior developers.'
            },
            {
                'name': 'Sita Thapa',
                'graduation_year': 2022,
                'current_position': 'Data Scientist',
                'company': 'Data Insights',
                'story': 'The training at Sipalaya Info Tech provided me with the perfect foundation for my career in data science. The practical approach and industry-relevant curriculum made all the difference.'
            }
        ]
        
        for data in stories_data:
            AlumniSuccessStory.objects.create(**data)
            self.stdout.write(f'Created alumni story: {data["name"]}')

    def create_team_members(self):
        team_data = [
            {
                'name': 'John Smith',
                'role': 'instructor',
                'designation': 'Senior Python Instructor',
                'bio': '10+ years of experience in Python development and teaching',
                'qualifications': 'MSc in Computer Science\nPython Certified Professional',
                'achievements': 'Trained 1000+ students\nPublished 3 technical books',
                'linkedin_url': 'https://linkedin.com/in/johnsmith',
                'github_url': 'https://github.com/johnsmith',
                'is_key_member': True
            },
            {
                'name': 'Sarah Johnson',
                'role': 'management',
                'designation': 'Academic Director',
                'bio': '15+ years of experience in education management',
                'qualifications': 'PhD in Education\nMBA in Educational Leadership',
                'achievements': 'Led curriculum development for 50+ courses\nEstablished partnerships with 20+ companies',
                'linkedin_url': 'https://linkedin.com/in/sarahjohnson',
                'is_key_member': True
            }
        ]
        
        for data in team_data:
            TeamMember.objects.create(**data)
            self.stdout.write(f'Created team member: {data["name"]}')

    def create_milestones(self):
        milestones_data = [
            {
                'title': 'Institution Founded',
                'description': 'Sipalaya Info Tech was established with a vision to provide quality IT education',
                'date': timezone.now().date().replace(year=2015),
                'icon': 'fas fa-flag'
            },
            {
                'title': 'First Batch Graduation',
                'description': 'First batch of students successfully completed their training',
                'date': timezone.now().date().replace(year=2016),
                'icon': 'fas fa-graduation-cap'
            },
            {
                'title': 'Industry Partnership Program',
                'description': 'Launched partnership program with leading IT companies',
                'date': timezone.now().date().replace(year=2017),
                'icon': 'fas fa-handshake'
            }
        ]
        
        for data in milestones_data:
            Milestone.objects.create(**data)
            self.stdout.write(f'Created milestone: {data["title"]}')

    def create_partnerships_and_certifications(self):
        # Create partnerships
        partnerships_data = [
            {
                'name': 'Tech Solutions Inc.',
                'type': 'company',
                'description': 'Leading software development company',
                'website_url': 'https://techsolutions.com',
                'partnership_date': timezone.now().date().replace(year=2020)
            },
            {
                'name': 'Python Institute',
                'type': 'certification',
                'description': 'Official Python certification body',
                'website_url': 'https://pythoninstitute.org',
                'partnership_date': timezone.now().date().replace(year=2021)
            }
        ]
        
        created_partnerships = []
        for data in partnerships_data:
            partnership = Partnership.objects.create(**data)
            created_partnerships.append(partnership)
            self.stdout.write(f'Created partnership: {partnership.name}')

        # Create certifications
        certifications_data = [
            {
                'name': 'Python Programming Professional',
                'provider': created_partnerships[1],
                'description': 'Comprehensive Python programming certification',
                'validity_period': 24,
                'is_featured': True
            },
            {
                'name': 'Web Development Expert',
                'provider': created_partnerships[0],
                'description': 'Advanced web development certification',
                'validity_period': 36,
                'is_featured': True
            }
        ]
        
        for data in certifications_data:
            Certification.objects.create(**data)
            self.stdout.write(f'Created certification: {data["name"]}')

    def create_demo_classes_and_bookings(self, students):
        courses = Course.objects.all()
        
        for course in courses:
            # Create demo class
            demo_class = DemoClass.objects.create(
                course=course,
                date=timezone.now().date() + timedelta(days=7),
                time=timezone.now().time().replace(hour=10, minute=0),
                capacity=20
            )
            self.stdout.write(f'Created demo class for: {course.title}')

            # Create some bookings
            for student in random.sample(list(students), 5):
                DemoClassBooking.objects.create(
                    demo_class=demo_class,
                    student=student
                )
                self.stdout.write(f'Created demo class booking for: {student.email}')

    def create_course_reviews(self, students):
        courses = Course.objects.all()
        
        for course in courses:
            # Create 3-5 reviews for each course
            for student in random.sample(list(students), random.randint(3, 5)):
                Review.objects.create(
                    student=student,
                    course=course,
                    rating=random.randint(4, 5),
                    comment=f'Great course! Learned a lot about {course.title}. The instructor was very helpful and the content was well-structured.'
                )
                self.stdout.write(f'Created review for {course.title} by {student.email}')

    def create_course_certificates(self, students):
        courses = Course.objects.all()
        
        for course in courses:
            # Create certificates for 2-3 students per course
            for student in random.sample(list(students), random.randint(2, 3)):
                Certificate.objects.create(
                    student=student,
                    course=course
                )
                self.stdout.write(f'Created certificate for {student.email} in {course.title}') 