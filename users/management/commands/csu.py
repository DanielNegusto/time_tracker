from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Create a superuser with predefined credentials"

    def handle(self, *args, **kwargs):
        username = "admin"
        password = "admin"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully.')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
