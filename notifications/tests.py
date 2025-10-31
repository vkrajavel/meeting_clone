from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User

class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')

    def test_signup(self):
        url = reverse('signup')
        data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'newpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)