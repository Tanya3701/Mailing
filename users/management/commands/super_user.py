import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv()


EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email=EMAIL)
        user.set_password(PASSWORD)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
