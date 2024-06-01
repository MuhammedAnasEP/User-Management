from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer
import json

class TestSetup(TestCase):
    def setUp(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'company_name': 'Inc.',
            'age': 30,
            'city': 'india',
            'state': 'test',
            'zip': 12345,
            'email': 'user@test.com',
            'web': 'http://test.com'
        }
        self.user = UserProfile.objects.create(**data)

    def bearer_token(self):
        """
        Generates a bearer token for the testing.
        """
        user = User.objects.create_user(username='adminuser', password='admin')
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
    


class UserProfileAPITests(TestSetup):
    def test_list_user_profiles(self):
        """
        Test the list_user_profiles endpoint of the API.
        This function sends a GET request to the 'users:users-list' URL and asserts that the response status code is 200.
        """
        url = reverse('users:users-list')
        headers = self.bearer_token()
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)

    def test_create_user_profile(self):
        """
        Test the create_user_profile function.
        This function tests the functionality of the create_user_profile method in the UserProfileAPITests class.
        It sends a POST request to the 'users:users-list' URL with the provided data and checks if the response status code is 201.
        It also checks if a UserProfile object with the provided email exists in the database.
        """
        url = reverse('users:users-list')
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'company_name': 'Inc.',
            'age': 30,
            'city': 'india',
            'state': 'test',
            'zip': 12345,
            'email': 'testuser@test.com',
            'web': 'http://test.com'
        }
        headers = self.bearer_token()
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserProfile.objects.filter(email=data['email']).exists())

    def test_retrieve_user_profile(self):
        """
        Test the retrieval of a user's profile.
        This function sends a GET request to the 'users:users-details' URL with the user's ID as a parameter.
        It adds the bearer token to the request headers.
        It asserts that the response status code is 200 (OK).
        It serializes the user's profile data using the UserProfileSerializer and compares it with the response data.
        """
        url = reverse('users:users-details', kwargs={'id': self.user.id})
        headers = self.bearer_token()
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = UserProfileSerializer(instance=self.user).data
        self.assertEqual(response.data, expected_data)

    def test_update_user_profile(self):
        """
        Test the update_user_profile function.
        This function sends a PUT request to the 'users:users-details' URL with the user's ID as a parameter.
        It updates the user's first name, last name, and age in the request data.
        It adds the bearer token to the request headers.
        It asserts that the response status code is 200 (OK).
        """
        url = reverse('users:users-details', kwargs={'id': self.user.id})
        data = {
            'first_name': 'updated',
            'last_name': 'to',
            'age': 35
            }
        headers = self.bearer_token()
        response = self.client.put(url, data=json.dumps(data), **headers, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'updated')
        self.assertEqual(self.user.age, 35)

    def test_delete_user_profile(self):
        """
        Test the delete_user_profile function.
        This function tests the functionality of the delete_user_profile method in the UserProfileAPITests class.
        It sends a DELETE request to the 'users:users-details' URL with the user's ID as a parameter.        
        """
        url = reverse('users:users-details', kwargs={'id': self.user.id})
        headers = self.bearer_token()
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(UserProfile.objects.filter(id=self.user.id).exists())
