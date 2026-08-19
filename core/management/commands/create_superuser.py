import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SU_NAME', 'admin')
        email = os.environ.get('DJANGO_SU_EMAIL', 'admin@nwz.com')
        password = os.environ.get('DJANGO_SU_PASSWORD')

        if not password:
            self.stdout.write('DJANGO_SU_PASSWORD not set — skipping superuser creation')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists — skipping')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f'Superuser "{username}" created successfully')