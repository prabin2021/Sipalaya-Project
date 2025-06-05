import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import TeamMember
import tempfile

class Command(BaseCommand):
    help = 'Populates the database with sample team members'

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
        self.stdout.write('Starting team members population...')

        # Create directory for team photos
        os.makedirs('media/team', exist_ok=True)

        # Sample team member data
        team_data = [
            {
                'name': 'Rajesh Sharma',
                'role': 'management',
                'designation': 'Founder & CEO',
                'image_url': 'https://images.unsplash.com/photo-1568602471122-7832951cc4c5',
                'bio': 'With over 15 years of experience in the tech industry, Rajesh leads our organization with a vision to transform education in Nepal.',
                'qualifications': 'MSc in Computer Science, Harvard University\nBSc in Computer Engineering, IIT Delhi',
                'achievements': '• Founded 3 successful tech startups\n• Published 5 research papers\n• Speaker at 20+ international conferences',
                'linkedin_url': 'https://linkedin.com/in/rajesh-sharma',
                'github_url': 'https://github.com/rajesh-sharma',
                'is_key_member': True,
                'order': 1
            },
            {
                'name': 'Priya Patel',
                'role': 'management',
                'designation': 'Head of Education',
                'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2',
                'bio': 'Priya brings 12 years of experience in curriculum development and educational technology.',
                'qualifications': 'PhD in Education Technology, Stanford University\nMEd in Curriculum Design, Columbia University',
                'achievements': '• Developed curriculum for 50+ tech courses\n• Led educational initiatives in 10+ countries\n• Awarded "Best Educator 2023"',
                'linkedin_url': 'https://linkedin.com/in/priya-patel',
                'github_url': '',
                'is_key_member': True,
                'order': 2
            },
            {
                'name': 'Amit Kumar',
                'role': 'instructor',
                'designation': 'Technical Director',
                'image_url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a',
                'bio': 'Amit is a full-stack developer with expertise in modern web technologies and cloud architecture.',
                'qualifications': 'MSc in Software Engineering, MIT\nAWS Solutions Architect\nGoogle Cloud Professional',
                'achievements': '• Built scalable applications for Fortune 500 companies\n• Contributed to 100+ open source projects\n• Author of "Modern Web Development"',
                'linkedin_url': 'https://linkedin.com/in/amit-kumar',
                'github_url': 'https://github.com/amit-kumar',
                'is_key_member': True,
                'order': 3
            }
        ]

        for idx, data in enumerate(team_data):
            member, created = TeamMember.objects.get_or_create(
                name=data['name'],
                defaults={
                    'role': data['role'],
                    'designation': data['designation'],
                    'bio': data['bio'],
                    'qualifications': data['qualifications'],
                    'achievements': data['achievements'],
                    'linkedin_url': data['linkedin_url'],
                    'github_url': data['github_url'],
                    'is_key_member': data['is_key_member'],
                    'order': data['order']
                }
            )
            
            if created:
                # Download and save team member photo
                img_temp = self.download_and_save_image(data['image_url'], f'team/member_{idx}.jpg')
                if img_temp:
                    member.photo.save(f'member_{idx}.jpg', File(img_temp))
                    img_temp.close()
                self.stdout.write(f'Created team member: {member.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated team members')) 