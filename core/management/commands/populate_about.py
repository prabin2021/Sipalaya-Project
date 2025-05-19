from django.core.management.base import BaseCommand
from core.models import CompanyInfo
from datetime import date

class Command(BaseCommand):
    help = 'Populates the database with company information'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting company information population...')

        company_info, created = CompanyInfo.objects.get_or_create(
            id=1,
            defaults={
                'mission': 'To empower individuals with cutting-edge technology education and skills for a better future.',
                'vision': 'To be the leading provider of technology education and career development in Nepal.',
                'history': '''Founded in 2020, Sipalaya Tech has been at the forefront of technology education in Nepal. 
                Our journey began with a simple yet powerful vision: to bridge the gap between traditional education and industry requirements.
                
                Over the years, we have:
                - Trained over 1000+ students in various technology domains
                - Established partnerships with leading tech companies
                - Developed industry-aligned curriculum
                - Created a strong alumni network
                - Achieved 90% placement rate for our graduates
                
                Our commitment to quality education and practical learning has made us a trusted name in technology education.''',
                'established_date': date(2020, 1, 1)
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created company information'))
        else:
            self.stdout.write(self.style.SUCCESS('Company information already exists')) 