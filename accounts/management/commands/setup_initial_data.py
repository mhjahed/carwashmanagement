from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from carwash.models import ServiceType
from accounts.models import User

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up initial data for the car wash management system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@carwash.com',
                password='admin123',
                first_name='Super',
                last_name='Admin',
                role='superadmin'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin/admin123')
            )
        else:
            self.stdout.write('Superuser already exists')
        
        # Create sample author
        if not User.objects.filter(username='author').exists():
            User.objects.create_user(
                username='author',
                email='author@carwash.com',
                password='author123',
                first_name='John',
                last_name='Author',
                role='author',
                phone='+8801234567890',
                post='Manager'
            )
            self.stdout.write(
                self.style.SUCCESS('Author created: author/author123')
            )
        else:
            self.stdout.write('Author already exists')
        
        # Create sample employer
        if not User.objects.filter(username='employer').exists():
            User.objects.create_user(
                username='employer',
                email='employer@carwash.com',
                password='employer123',
                first_name='Jane',
                last_name='Employer',
                role='employer',
                phone='+8801234567891',
                post='Car Washer'
            )
            self.stdout.write(
                self.style.SUCCESS('Employer created: employer/employer123')
            )
        else:
            self.stdout.write('Employer already exists')
        
        # Create service types
        services = [
            {'name': 'Basic Wash', 'description': 'Exterior wash only', 'price': 200.00},
            {'name': 'Premium Wash', 'description': 'Exterior + Interior cleaning', 'price': 400.00},
            {'name': 'Full Service', 'description': 'Complete wash + wax + interior', 'price': 600.00},
            {'name': 'Express Wash', 'description': 'Quick exterior wash', 'price': 150.00},
        ]
        
        for service_data in services:
            service, created = ServiceType.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Service created: {service.name}')
                )
            else:
                self.stdout.write(f'Service already exists: {service.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Initial data setup completed!')
        )
