from django.test import TestCase
from django.urls import reverse
from videoflix.users.models import CustomUser
# from django.contrib.auth import get_user_model

# Create your tests here.


class UserAccountTests(TestCase):
    # register user
    def test_registration(self):
        response = self.client.post(reverse('register'), data={
            'email': 'test@test.de',
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertTrue(CustomUser.objects.filter(email='test@test.de').exists())
        
    
    # register and login
    def lest_login(self):
        response = self.client.post(reverse('register'), data={
            'email': 'test@test.de',
            'username': 'testuser',
            'password': 'testpass123'
        })
        loggedIn = self.client.post(reverse('login'), data={
            'email': 'test@test.de',
            'password': 'testpass123'
        })
        