import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from careers.models import AlumniSuccessStory
import tempfile

class Command(BaseCommand):
    help = 'Populates the database with sample alumni success stories'

    def download_and_save_image(self, url, save_path):
        """Downloads an image from URL and saves it to the specified path."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_temp = tempfile.NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                return img_temp
            return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to download image: {str(e)}'))
            return None

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting alumni success stories population...')

        # Create directory for alumni photos
        os.makedirs('media/alumni_stories', exist_ok=True)

        # Sample alumni data
        alumni_data = [
            {
                'name': 'Rajesh Sharma',
                'graduation_year': 2022,
                'current_position': 'Senior Software Engineer',
                'company': 'Tech Solutions Nepal',
                'image_url': 'https://images.unsplash.com/photo-1568602471122-7832951cc4c5',
                'story': 'After completing the Python and Django course at Sipalaya Tech, I was able to land my dream job as a software engineer. The practical projects and mentorship provided during the course were invaluable in preparing me for the industry.'
            },
            {
                'name': 'Priya Patel',
                'graduation_year': 2023,
                'current_position': 'Data Scientist',
                'company': 'AI Innovations',
                'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2',
                'story': 'The Data Science course at Sipalaya Tech gave me the skills and confidence to transition from a traditional IT role to a data science position. The hands-on projects and real-world case studies were particularly helpful.'
            },
            {
                'name': 'Amit Kumar',
                'graduation_year': 2021,
                'current_position': 'Full Stack Developer',
                'company': 'Digital Solutions',
                'image_url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a',
                'story': 'Starting with no prior programming experience, the Web Development Bootcamp at Sipalaya Tech helped me build a strong foundation. Within a year of graduation, I was leading a team of developers.'
            },
            {
                'name': 'Sita Thapa',
                'graduation_year': 2023,
                'current_position': 'DevOps Engineer',
                'company': 'Cloud Tech Solutions',
                'image_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956',
                'story': 'The Cloud Computing course at Sipalaya Tech opened up new career opportunities for me. The practical experience with AWS and Docker was exactly what employers were looking for.'
            },
            {
                'name': 'Bikram Gurung',
                'graduation_year': 2022,
                'current_position': 'Mobile App Developer',
                'company': 'AppWorks Nepal',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
                'story': 'The Mobile Development course at Sipalaya Tech helped me launch my career in app development. The project-based learning approach gave me the confidence to build and publish my own apps.'
            }
        ]

        for idx, data in enumerate(alumni_data):
            alumni, created = AlumniSuccessStory.objects.get_or_create(
                name=data['name'],
                defaults={
                    'graduation_year': data['graduation_year'],
                    'current_position': data['current_position'],
                    'company': data['company'],
                    'story': data['story']
                }
            )
            
            if created:
                # Download and save alumni photo
                img_temp = self.download_and_save_image(data['image_url'], f'alumni_stories/alumni_{idx}.jpg')
                if img_temp:
                    alumni.image.save(f'alumni_{idx}.jpg', File(img_temp))
                    img_temp.close()
                self.stdout.write(f'Created alumni success story: {alumni.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated alumni success stories')) 