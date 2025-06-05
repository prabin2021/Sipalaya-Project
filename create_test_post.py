import os
import django
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

from blog.models import BlogPost, Category
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_post():
    # Get or create a test category
    category, created = Category.objects.get_or_create(
        name='Technology',
        defaults={
            'description': 'Posts about technology and programming'
        }
    )
    
    # Get the user
    user = User.objects.filter(email='sigdelprabin321@gmail.com').first()
    
    if not user:
        print("User not found with email: sigdelprabin321@gmail.com")
        return
    
    # Create a test post
    post = BlogPost.objects.create(
        title='Welcome to Our Blog',
        author=user,
        category=category,
        content='This is a test blog post to ensure everything is working correctly.',
        excerpt='A test post for our blog system.',
        status='published',
        published_at=timezone.now()
    )
    
    print(f"\nCreated test post:")
    print(f"Title: {post.title}")
    print(f"Author: {post.author.email}")
    print(f"Category: {post.category.name}")
    print(f"Status: {post.status}")
    print(f"Published at: {post.published_at}")

if __name__ == '__main__':
    create_test_post() 