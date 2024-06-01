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
        user = User.objects.create_user(username='adminuser', password='admin')
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
    
    

class UserProfileAPITests(TestSetup):

    def test_list_user_profiles(self):
        url = reverse('users:users-list')
        headers = self.bearer_token()
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)


    def test_create_user_profile(self):
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
        url = reverse('users:users-details', kwargs={'id': self.user.id})
        headers = self.bearer_token()
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = UserProfileSerializer(instance=self.user).data
        self.assertEqual(response.data, expected_data)


    def test_update_user_profile(self):
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
        url = reverse('users:users-details', kwargs={'id': self.user.id})
        headers = self.bearer_token()
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(UserProfile.objects.filter(id=self.user.id).exists())

    
