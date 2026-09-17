from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

class Command(BaseCommand):
    help = 'Seeds sample tasks into the database for demonstration'

    def handle(self, *args, **options):
        if Task.objects.exists():
            self.stdout.write(self.style.WARNING('Tasks already exist in the database.'))
            return

        today = timezone.now().date()
        sample_tasks = [
            {
                'title': 'Design Glassmorphism Dashboard UI',
                'description': 'Create responsive dashboard components with dark theme, neon accents, and metric widgets.',
                'priority': Task.Priority.HIGH,
                'status': Task.Status.COMPLETED,
                'category': Task.Category.DESIGN,
                'due_date': today - timedelta(days=1),
            },
            {
                'title': 'Implement Automated GitHub CI/CD Actions',
                'description': 'Set up GitHub Actions matrix to test against Python versions and run migrations check.',
                'priority': Task.Priority.HIGH,
                'status': Task.Status.COMPLETED,
                'category': Task.Category.DEVELOPMENT,
                'due_date': today,
            },
            {
                'title': 'Configure WhiteNoise & Gunicorn for Production',
                'description': 'Ensure static files are served efficiently with compressed manifest storage.',
                'priority': Task.Priority.MEDIUM,
                'status': Task.Status.IN_PROGRESS,
                'category': Task.Category.DEVELOPMENT,
                'due_date': today + timedelta(days=2),
            },
            {
                'title': 'Connect Remote GitHub Repository',
                'description': 'Create new repository on GitHub under user account and push initial main branch.',
                'priority': Task.Priority.HIGH,
                'status': Task.Status.PENDING,
                'category': Task.Category.WORK,
                'due_date': today + timedelta(days=1),
            },
            {
                'title': 'Deploy Live on Render Cloud Service',
                'description': 'Deploy using render.yaml blueprint with automatic SSL certificate and zero-downtime deploys.',
                'priority': Task.Priority.MEDIUM,
                'status': Task.Status.PENDING,
                'category': Task.Category.WORK,
                'due_date': today + timedelta(days=3),
            },
        ]

        for item in sample_tasks:
            Task.objects.create(**item)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(sample_tasks)} sample tasks!'))
