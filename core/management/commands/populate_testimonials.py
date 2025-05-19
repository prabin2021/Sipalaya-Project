import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Testimonial
import tempfile

class Command(BaseCommand):
    help = 'Populates the database with sample testimonials'

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
        self.stdout.write('Starting testimonials population...')

        # Create directory for testimonial photos
        os.makedirs('media/testimonials', exist_ok=True)

        # Sample testimonial data
        testimonial_data = [
            {
                'name': 'Rajesh Sharma',
                'position': 'Senior Software Engineer',
                'company': 'Tech Solutions Nepal',
                'image_url': 'https://images.unsplash.com/photo-1568602471122-7832951cc4c5',
                'content': 'The Python and Django course at Sipalaya Tech was a game-changer for my career. The practical projects and mentorship provided during the course were invaluable in preparing me for the industry.',
                'rating': 5
            },
            {
                'name': 'Priya Patel',
                'position': 'Data Scientist',
                'company': 'AI Innovations',
                'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2',
                'content': 'The Data Science course gave me the skills and confidence to transition from a traditional IT role to a data science position. The hands-on projects and real-world case studies were particularly helpful.',
                'rating': 5
            },
            {
                'name': 'Amit Kumar',
                'position': 'Full Stack Developer',
                'company': 'Digital Solutions',
                'image_url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a',
                'content': 'Starting with no prior programming experience, the Web Development Bootcamp helped me build a strong foundation. Within a year of graduation, I was leading a team of developers.',
                'rating': 5
            },
            {
                'name': 'Sita Thapa',
                'position': 'DevOps Engineer',
                'company': 'Cloud Tech Solutions',
                'image_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956',
                'content': 'The Cloud Computing course opened up new career opportunities for me. The practical experience with AWS and Docker was exactly what employers were looking for.',
                'rating': 5
            },
            {
                'name': 'Bikram Gurung',
                'position': 'Mobile App Developer',
                'company': 'AppWorks Nepal',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
                'content': 'The Mobile Development course helped me launch my career in app development. The project-based learning approach gave me the confidence to build and publish my own apps.',
                'rating': 5
            }
        ]

        for idx, data in enumerate(testimonial_data):
            testimonial, created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults={
                    'position': data['position'],
                    'company': data['company'],
                    'content': data['content'],
                    'rating': data['rating'],
                    'is_active': True
                }
            )
            
            if created:
                # Download and save testimonial photo
                img_temp = self.download_and_save_image(data['image_url'], f'testimonials/testimonial_{idx}.jpg')
                if img_temp:
                    testimonial.image.save(f'testimonial_{idx}.jpg', File(img_temp))
                    img_temp.close()
                self.stdout.write(f'Created testimonial: {testimonial.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated testimonials')) 