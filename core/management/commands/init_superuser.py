import os
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser account from .env file'

    def handle(self, *args, **kwargs):
        EMAIL = os.environ.get('DJANGO_ADMIN_EMAIL')
        USERNAME = os.environ.get('DJANGO_ADMIN_USERNAME')
        PASSWORD = os.environ.get('DJANGO_ADMIN_PASSWORD')
        EXIT_MSG_PATTERN = 'The environment variable {} is empty./n'

        exit_msg = ''

        if EMAIL is None:
            exit_msg += str.format(EXIT_MSG_PATTERN, 'DJANGO_ADMIN_EMAIL')
        if USERNAME is None:
            exit_msg += str.format(EXIT_MSG_PATTERN, 'DJANGO_ADMIN_USERNAME')
        if PASSWORD is None:
            exit_msg += str.format(EXIT_MSG_PATTERN, 'DJANGO_ADMIN_PASSWORD')
        if User.objects.filter(username=USERNAME).exists():
            exit_msg += 'The superuser account already exists'
        if exit_msg != '':
            self.stdout.write(
                self.style.ERROR(exit_msg)
            )
            sys.exit(1)
        User.objects.create_superuser(
            email=EMAIL,
            username=USERNAME,
            password=PASSWORD
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'The superuser account for {USERNAME} is created'
            )
        )
