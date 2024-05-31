import requests
from users.models import UserProfile
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate database with sample user data'

    def handle(self, *args, **kwargs):
        response = requests.get('https://datapeace-storage.s3-us-west-2.amazonaws.com/dummy_data/users.json')
        if response.status_code == 200:
            data = response.json()
            for user_data in data:
                UserProfile.objects.create(**user_data)
            self.stdout.write(self.style.SUCCESS('Successfully populated database'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data'))