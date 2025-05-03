import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sipalaya_Backend.settings')
django.setup()

from homepage.models import Banner, Feature, Contact

def populate_homepage():
    # Create Banners
    banners = [
        {
            'title': 'Master Web Development',
            'subtitle': 'Learn Full Stack Development with Python & React',
            'image': 'banners/banner1.jpg',
            'button_text': 'Enroll Now',
            'link': '/courses',
            'is_active': True,
            'order': 1
        },
        {
            'title': 'Special Offer: 10% Off!',
            'subtitle': 'Enroll in our January batch and get 10% discount on all courses',
            'image': 'banners/django.png',
            'button_text': 'View Courses',
            'link': '/courses',
            'is_active': True,
            'order': 2
        },
        {
            'title': 'New Python Course Launched',
            'subtitle': 'From basics to advanced - Start your programming journey today',
            'image': 'banners/react.png',
            'button_text': 'Schedule a Demo',
            'link': '/demo-classes',
            'is_active': True,
            'order': 3
        }
    ]

    for banner_data in banners:
        Banner.objects.create(**banner_data)
        print(f"Created banner: {banner_data['title']}")

    # Create Features
    features = [
        {
            'title': 'IT Training',
            'description': 'Comprehensive training in programming, web development, and more',
            'icon_class': 'fas fa-laptop-code'
        },
        {
            'title': 'Certification Prep',
            'description': 'Expert guidance for industry-recognized certifications',
            'icon_class': 'fas fa-certificate'
        },
        {
            'title': 'Corporate Workshops',
            'description': 'Customized training programs for corporate teams',
            'icon_class': 'fas fa-building'
        },
        {
            'title': '5000+ Students Trained',
            'description': 'Join our growing community of successful graduates',
            'icon_class': 'fas fa-users'
        },
        {
            'title': '90% Placement Rate',
            'description': 'Our graduates are placed in top tech companies',
            'icon_class': 'fas fa-briefcase'
        },
        {
            'title': 'Expert Mentors',
            'description': 'Learn from industry professionals with years of experience',
            'icon_class': 'fas fa-chalkboard-teacher'
        }
    ]

    for feature_data in features:
        Feature.objects.create(**feature_data)
        print(f"Created feature: {feature_data['title']}")

    # Create sample contact entries
    contacts = [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '9876543210',
            'message': 'Interested in Python course'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone_number': '9876543211',
            'message': 'Want to know about web development course'
        }
    ]

    for contact_data in contacts:
        Contact.objects.create(**contact_data)
        print(f"Created contact entry for: {contact_data['name']}")

if __name__ == '__main__':
    print("Starting homepage population...")
    populate_homepage()
    print("Homepage population completed!") 