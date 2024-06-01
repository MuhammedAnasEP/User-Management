import requests
from users.models import UserProfile
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate database with sample user data'

    def handle(self, *args, **kwargs):
        """
        Handles the command to populate the database with sample user data.
        This method sends a GET request to the specified URL to fetch the sample user data.
        If the request is successful (status code 200), the response JSON is parsed and
        each user data is used to create a new `UserProfile` object in the database.
        After populating the database, a success message is printed to the console.
        If the request fails (status code other than 200), an error message is printed to
        the console indicating that the data could not be fetched.
        """
        response = requests.get('https://datapeace-storage.s3-us-west-2.amazonaws.com/dummy_data/users.json')
        if response.status_code == 200:
            data = response.json()
            for user_data in data:
                UserProfile.objects.create(**user_data)
            self.stdout.write(self.style.SUCCESS('Successfully populated database'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data'))