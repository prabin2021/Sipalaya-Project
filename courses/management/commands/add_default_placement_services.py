from django.core.management.base import BaseCommand
from courses.models import PlacementService

class Command(BaseCommand):
    help = 'Adds default placement services'

    def handle(self, *args, **kwargs):
        services = [
            {
                'title': 'Career Counseling',
                'description': 'One-on-one career guidance sessions to help you identify your career goals and create a personalized career development plan.',
                'icon': 'fas fa-comments'
            },
            {
                'title': 'Resume Building',
                'description': 'Professional resume writing assistance and review to help you stand out to potential employers.',
                'icon': 'fas fa-file-alt'
            },
            {
                'title': 'Interview Preparation',
                'description': 'Mock interviews and interview skills training to help you ace your job interviews.',
                'icon': 'fas fa-handshake'
            },
            {
                'title': 'Job Placement',
                'description': 'Direct placement assistance with our partner companies and access to exclusive job opportunities.',
                'icon': 'fas fa-briefcase'
            },
            {
                'title': 'Networking Events',
                'description': 'Regular networking events with industry professionals and potential employers.',
                'icon': 'fas fa-users'
            },
            {
                'title': 'Skill Assessment',
                'description': 'Comprehensive skill assessment and gap analysis to help you identify areas for improvement.',
                'icon': 'fas fa-chart-line'
            }
        ]

        for service_data in services:
            PlacementService.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'icon': service_data['icon']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully added default placement services')) 