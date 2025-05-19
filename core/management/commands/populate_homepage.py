import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils import timezone
from core.models import (
    Banner, Statistic, Service, CompanyInfo, Milestone,
    TeamMember, Partnership, Certification
)
import tempfile
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populates the homepage with sample data'

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
        self.stdout.write('Starting homepage data population...')

        # Create banners
        banner_data = [
            {
                'title': 'Learn Python Programming',
                'subtitle': 'Master Python from basics to advanced concepts',
                'image_url': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935',
                'link': '/courses/python-programming/',
                'button_text': 'Start Learning'
            },
            {
                'title': 'Web Development Bootcamp',
                'subtitle': 'Become a full-stack web developer',
                'image_url': 'https://images.unsplash.com/photo-1547658719-da2b51169166',
                'link': '/courses/web-development/',
                'button_text': 'Enroll Now'
            },
            {
                'title': 'Data Science Career Path',
                'subtitle': 'Launch your career in data science',
                'image_url': 'https://images.unsplash.com/photo-1485796826113-174aa68fd81b',
                'link': '/courses/data-science/',
                'button_text': 'Learn More'
            }
        ]

        for idx, data in enumerate(banner_data):
            banner, created = Banner.objects.get_or_create(
                title=data['title'],
                defaults={
                    'subtitle': data['subtitle'],
                    'link': data['link'],
                    'button_text': data['button_text'],
                    'order': idx
                }
            )
            
            if created:
                img_temp = self.download_and_save_image(data['image_url'], f'banners/banner_{idx}.jpg')
                if img_temp:
                    banner.image.save(f'banner_{idx}.jpg', File(img_temp))
                    img_temp.close()
                self.stdout.write(f'Created banner: {banner.title}')

        # Create statistics
        statistics = [
            {'title': 'Students Enrolled', 'value': 5000, 'icon': 'fa-users'},
            {'title': 'Courses Available', 'value': 50, 'icon': 'fa-book'},
            {'title': 'Expert Instructors', 'value': 25, 'icon': 'fa-chalkboard-teacher'},
            {'title': 'Success Rate', 'value': 95, 'icon': 'fa-chart-line'}
        ]

        for idx, stat in enumerate(statistics):
            statistic, created = Statistic.objects.get_or_create(
                title=stat['title'],
                defaults={
                    'value': stat['value'],
                    'icon': stat['icon'],
                    'order': idx
                }
            )
            if created:
                self.stdout.write(f'Created statistic: {statistic.title}')

        # Create services
        services = [
            {
                'title': 'Online Learning',
                'description': 'Access courses anytime, anywhere with our flexible online learning platform.',
                'icon': 'fa-laptop'
            },
            {
                'title': 'Expert Instructors',
                'description': 'Learn from industry experts with years of practical experience.',
                'icon': 'fa-chalkboard-teacher'
            },
            {
                'title': 'Career Support',
                'description': 'Get guidance on career paths, job opportunities, and industry trends.',
                'icon': 'fa-briefcase'
            },
            {
                'title': 'Certification',
                'description': 'Earn recognized certificates to boost your career prospects.',
                'icon': 'fa-certificate'
            }
        ]

        for idx, service in enumerate(services):
            service_obj, created = Service.objects.get_or_create(
                title=service['title'],
                defaults={
                    'description': service['description'],
                    'icon': service['icon'],
                    'order': idx
                }
            )
            if created:
                self.stdout.write(f'Created service: {service_obj.title}')

        # Create company info
        company_info, created = CompanyInfo.objects.get_or_create(
            id=1,
            defaults={
                'mission': 'To empower individuals with cutting-edge technology education and skills for a better future.',
                'vision': 'To be the leading provider of technology education and career development in Nepal.',
                'history': 'Founded in 2020, Sipalaya Info Tech has been at the forefront of technology education, helping thousands of students achieve their career goals.',
                'established_date': date(2020, 1, 1)
            }
        )
        if created:
            self.stdout.write('Created company information')

        # Create milestones
        milestones = [
            {
                'title': 'Company Founded',
                'description': 'Sipalaya Info Tech was established with a vision to transform technology education.',
                'date': date(2020, 1, 1),
                'icon': 'fa-flag'
            },
            {
                'title': 'First Course Launch',
                'description': 'Launched our first Python programming course.',
                'date': date(2020, 3, 1),
                'icon': 'fa-rocket'
            },
            {
                'title': '1000 Students',
                'description': 'Reached milestone of 1000 enrolled students.',
                'date': date(2021, 6, 1),
                'icon': 'fa-users'
            },
            {
                'title': 'Partnership Program',
                'description': 'Started industry partnerships for better career opportunities.',
                'date': date(2022, 1, 1),
                'icon': 'fa-handshake'
            }
        ]

        for idx, milestone in enumerate(milestones):
            milestone_obj, created = Milestone.objects.get_or_create(
                title=milestone['title'],
                defaults={
                    'description': milestone['description'],
                    'date': milestone['date'],
                    'icon': milestone['icon'],
                    'order': idx
                }
            )
            if created:
                self.stdout.write(f'Created milestone: {milestone_obj.title}')

        # Create team members
        team_data = [
            {
                'name': 'John Doe',
                'role': 'instructor',
                'designation': 'Senior Python Instructor',
                'image_url': 'https://images.unsplash.com/photo-1568602471122-7832951cc4c5',
                'bio': '10+ years of experience in Python development and teaching.',
                'qualifications': 'MSc in Computer Science, Python Certified Developer',
                'achievements': 'Published author, Speaker at PyCon',
                'linkedin_url': 'https://linkedin.com/in/johndoe',
                'github_url': 'https://github.com/johndoe',
                'is_key_member': True
            },
            {
                'name': 'Jane Smith',
                'role': 'management',
                'designation': 'Academic Director',
                'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2',
                'bio': '15+ years of experience in education management.',
                'qualifications': 'PhD in Education, MBA',
                'achievements': 'Education Excellence Award 2022',
                'linkedin_url': 'https://linkedin.com/in/janesmith',
                'is_key_member': True
            }
        ]

        for idx, member in enumerate(team_data):
            team_member, created = TeamMember.objects.get_or_create(
                name=member['name'],
                defaults={
                    'role': member['role'],
                    'designation': member['designation'],
                    'bio': member['bio'],
                    'qualifications': member['qualifications'],
                    'achievements': member['achievements'],
                    'linkedin_url': member.get('linkedin_url', ''),
                    'github_url': member.get('github_url', ''),
                    'is_key_member': member['is_key_member'],
                    'order': idx
                }
            )
            
            if created:
                img_temp = self.download_and_save_image(member['image_url'], f'team/member_{idx}.jpg')
                if img_temp:
                    team_member.photo.save(f'member_{idx}.jpg', File(img_temp))
                    img_temp.close()
                self.stdout.write(f'Created team member: {team_member.name}')

        # Create partnerships
        partnership_data = [
            {
                'name': 'Tech Solutions Nepal',
                'type': 'company',
                'logo_url': 'https://images.unsplash.com/photo-1560179707-f14e90ef3623',
                'description': 'Leading IT company in Nepal',
                'website_url': 'https://techsolutions.com.np',
                'partnership_date': date(2021, 1, 1)
            },
            {
                'name': 'Python Institute',
                'type': 'certification',
                'logo_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5',
                'description': 'Global Python certification body',
                'website_url': 'https://pythoninstitute.org',
                'partnership_date': date(2021, 3, 1)
            }
        ]

        for idx, partner in enumerate(partnership_data):
            partnership, created = Partnership.objects.get_or_create(
                name=partner['name'],
                defaults={
                    'type': partner['type'],
                    'description': partner['description'],
                    'website_url': partner['website_url'],
                    'partnership_date': partner['partnership_date'],
                    'order': idx
                }
            )
            
            if created:
                img_temp = self.download_and_save_image(partner['logo_url'], f'partners/partner_{idx}.jpg')
                if img_temp:
                    partnership.logo.save(f'partner_{idx}.jpg', File(img_temp))
                    img_temp.close()
                self.stdout.write(f'Created partnership: {partnership.name}')

                # Create certification for certification partners
                if partner['type'] == 'certification':
                    certification, created = Certification.objects.get_or_create(
                        name=f'{partner["name"]} Certification',
                        provider=partnership,
                        defaults={
                            'description': f'Professional certification from {partner["name"]}',
                            'is_featured': True
                        }
                    )
                    if created:
                        self.stdout.write(f'Created certification: {certification.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated homepage data')) 