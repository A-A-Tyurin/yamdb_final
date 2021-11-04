import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Fill the database from .csv files'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', action='store_true',
                            help='Upload users from users.csv')

    def handle(self, *args, **kwargs):
        user = kwargs.get('user')

        if user:
            try:
                with open(
                    'static/data/users.csv', encoding='utf-8'
                ) as csvfile:
                    if csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            User.objects.create(**row)
                        self.stdout.write(
                            self.style.SUCCESS(
                                'The users are uploaded to the database.'
                            )
                        )
            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR('The file users.csv not found.')
                )
