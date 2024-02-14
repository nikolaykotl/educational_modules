import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email= os.getenv('EMAIL'),
            first_name= os.getenv('FIRST_NAME'),
            last_name= os.getenv('LAST_NAME'),
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('PASSWORD'))
        user.save()
