import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sipalaya_Backend.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Category, Course

def create_categories():
    categories = [
        {
            'name': 'Programming',
            'description': 'Learn programming languages and software development'
        },
        {
            'name': 'Web Development',
            'description': 'Master web technologies and frameworks'
        },
        {
            'name': 'Data Science',
            'description': 'Learn data analysis and machine learning'
        },
        {
            'name': 'Graphic Design',
            'description': 'Master design tools and principles'
        }
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(**cat_data)
        print(f"Created category: {cat_data['name']}")

def create_courses():
    # Get or create instructor
    instructor, _ = User.objects.get_or_create(
        username='instructor1',
        defaults={
            'email': 'instructor@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    )
    
    # Get categories
    programming = Category.objects.get(name='Programming')
    web_dev = Category.objects.get(name='Web Development')
    data_science = Category.objects.get(name='Data Science')
    design = Category.objects.get(name='Graphic Design')
    
    courses = [
        {
            'title': 'Python Programming',
            'description': 'Learn Python from basics to advanced concepts',
            'category': programming,
            'instructor': instructor,
            'skill_level': 'beginner',
            'duration': 'medium',
            'price': 15000,
            'syllabus': 'Introduction to Python\nData Types\nControl Structures\nFunctions\nObject-Oriented Programming\nFile Handling\nModules and Packages',
            'prerequisites': 'Basic computer knowledge\nNo prior programming experience required'
        },
        {
            'title': 'Full Stack Web Development',
            'description': 'Master frontend and backend web development',
            'category': web_dev,
            'instructor': instructor,
            'skill_level': 'intermediate',
            'duration': 'long',
            'price': 25000,
            'syllabus': 'HTML5 & CSS3\nJavaScript\nReact.js\nNode.js\nExpress.js\nMongoDB\nRESTful APIs',
            'prerequisites': 'Basic understanding of programming\nFamiliarity with HTML/CSS'
        },
        {
            'title': 'Data Science with Python',
            'description': 'Learn data analysis and machine learning',
            'category': data_science,
            'instructor': instructor,
            'skill_level': 'intermediate',
            'duration': 'long',
            'price': 30000,
            'syllabus': 'Python for Data Science\nNumPy & Pandas\nData Visualization\nMachine Learning\nDeep Learning\nProject Work',
            'prerequisites': 'Basic Python knowledge\nUnderstanding of statistics'
        },
        {
            'title': 'Adobe Photoshop Masterclass',
            'description': 'Master professional photo editing and design',
            'category': design,
            'instructor': instructor,
            'skill_level': 'beginner',
            'duration': 'medium',
            'price': 20000,
            'syllabus': 'Interface Overview\nBasic Tools\nLayers & Masks\nColor Correction\nPhoto Retouching\nDesign Principles\nProject Work',
            'prerequisites': 'Basic computer skills\nNo prior design experience required'
        }
    ]
    
    for course_data in courses:
        Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        print(f"Created course: {course_data['title']}")

if __name__ == '__main__':
    print("Starting course population...")
    create_categories()
    create_courses()
    print("Course population completed!") 