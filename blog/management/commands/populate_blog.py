import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, BlogPost

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the blog with sample data'

    def download_and_save_image(self, url, path):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                return File(img_temp, name=os.path.basename(path))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to download image: {e}'))
        return None

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting blog population...')

        # Create directory for blog images if it doesn't exist
        os.makedirs('media/blog', exist_ok=True)

        # Create categories
        categories = [
            'Technology',
            'Career Development',
            'Education',
            'Industry Insights'
        ]
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Articles about {cat_name.lower()}'}
            )
            if created:
                self.stdout.write(f'Created category: {cat_name}')

        # Create tags
        tags = [
            'Python',
            'Web Development',
            'Data Science',
            'Career Tips',
            'Cloud Computing',
            'AI/ML',
            'Interview Preparation'
        ]
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')

        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@sipalayainfotech.com',
            defaults={
                'username': 'blog_admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user')

        # Sample blog posts
        blog_posts = [
            {
                'title': 'Getting Started with Python Programming',
                'content': '''
                Python is one of the most popular programming languages today, known for its simplicity and versatility. In this article, we'll explore why Python is an excellent choice for beginners and how to get started with your first Python program.

                ## Why Learn Python?

                Python offers several advantages for beginners:
                - Easy to read and write syntax
                - Extensive library support
                - Large and active community
                - Versatile applications (web development, data science, AI, etc.)

                ## Setting Up Your Environment

                To begin your Python journey, you'll need to:
                1. Install Python from python.org
                2. Choose a code editor (VS Code recommended)
                3. Set up a virtual environment

                ## Your First Python Program

                Let's write a simple "Hello, World!" program:
                ```python
                print("Hello, World!")
                ```

                This is just the beginning of your Python journey. Stay tuned for more articles on Python programming!
                ''',
                'excerpt': 'A beginner-friendly guide to starting your Python programming journey.',
                'category': 'Technology',
                'tags': ['Python', 'Web Development'],
                'image_url': 'https://images.unsplash.com/photo-1526379879527-8559ecfcaec4'
            },
            {
                'title': 'Career Paths in Data Science',
                'content': '''
                Data Science has emerged as one of the most promising career paths in technology. This article explores various roles and opportunities in the field of data science.

                ## Popular Data Science Roles

                1. Data Analyst
                2. Data Scientist
                3. Machine Learning Engineer
                4. Data Engineer
                5. Business Intelligence Analyst

                ## Required Skills

                To succeed in data science, you should focus on:
                - Programming (Python, R)
                - Statistics and Mathematics
                - Machine Learning
                - Data Visualization
                - Domain Knowledge

                ## Getting Started

                Begin your data science journey by:
                1. Learning Python programming
                2. Understanding basic statistics
                3. Exploring data analysis libraries
                4. Building a portfolio of projects

                Stay tuned for more articles on data science careers and skills!
                ''',
                'excerpt': 'Explore various career opportunities in the field of data science.',
                'category': 'Career Development',
                'tags': ['Data Science', 'Career Tips', 'AI/ML'],
                'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71'
            },
            {
                'title': 'Cloud Computing: The Future of IT Infrastructure',
                'content': '''
                Cloud computing has revolutionized how businesses manage their IT infrastructure. This article discusses the impact and future of cloud computing.

                ## What is Cloud Computing?

                Cloud computing is the delivery of computing services over the internet, including:
                - Servers
                - Storage
                - Databases
                - Networking
                - Software

                ## Benefits of Cloud Computing

                Key advantages include:
                - Cost efficiency
                - Scalability
                - Flexibility
                - Disaster recovery
                - Automatic updates

                ## Popular Cloud Platforms

                Major cloud providers include:
                1. Amazon Web Services (AWS)
                2. Microsoft Azure
                3. Google Cloud Platform (GCP)

                Learn more about cloud computing in our upcoming articles!
                ''',
                'excerpt': 'Understanding the impact and future of cloud computing in modern IT infrastructure.',
                'category': 'Technology',
                'tags': ['Cloud Computing', 'Web Development'],
                'image_url': 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8'
            }
        ]

        # Create blog posts
        for post_data in blog_posts:
            category = Category.objects.get(name=post_data['category'])
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'author': admin_user,
                    'category': category,
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'status': 'published',
                    'published_at': timezone.now()
                }
            )
            
            if created:
                # Add tags
                for tag_name in post_data['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    post.tags.add(tag)
                
                # Download and save featured image
                if post_data.get('image_url'):
                    image_path = f'blog/{post.slug}.jpg'
                    image_file = self.download_and_save_image(post_data['image_url'], image_path)
                    if image_file:
                        post.featured_image.save(image_path, image_file, save=True)
                
                self.stdout.write(f'Created blog post: {post.title}')
            else:
                self.stdout.write(f'Blog post already exists: {post.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated blog with sample data')) 