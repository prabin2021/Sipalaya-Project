import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

from django.contrib.auth import get_user_model
from instructor.models import InstructorProfile

User = get_user_model()

def check_user_type():
    # Get the user
    user = User.objects.filter(email='sigdelprabin321@gmail.com').first()
    
    if not user:
        print("User not found with email: sigdelprabin321@gmail.com")
        return
    
    # Check if user is an instructor
    is_instructor = hasattr(user, 'instructor_profile') or user.courses_teaching.exists()
    
    print(f"\nUser: {user.email}")
    print(f"Is instructor: {is_instructor}")
    print(f"Has instructor profile: {hasattr(user, 'instructor_profile')}")
    print(f"Teaching courses: {user.courses_teaching.exists()}")

if __name__ == '__main__':
    check_user_type() 