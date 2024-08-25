import os
from django.test import Client, TestCase
from django.urls import reverse

from users.views import reset_password, send_activation_email
from .models import CustomUser
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import ANY, patch
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class UserAccountTests(TestCase):
    """
    Test for user account operations including registration, login, and logout.
    """
    def setUp(self):
        self.client = APIClient()

    @patch.object(EmailMultiAlternatives, 'send', return_value=None)
    def test_register_user(self, mock_send):
        register_response = self.client.post(reverse('register'), data={
            'email': 'test@test.de',
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(register_response.status_code, 200)
        user = CustomUser.objects.get(email='test@test.de')
        user.is_active = True
        user.save()
        print("User created and active OK")

    def test_login_user(self):
        self.client.post(reverse('register'), data={
            'email': 'test@test.de',
            'username': 'testuser',
            'password': 'testpassword123'
        })
        user = CustomUser.objects.get(email='test@test.de')
        user.is_active = True
        user.save()
        login_response = self.client.post(reverse('login'), data={
            'email': 'test@test.de',
            'password': 'testpassword123'
        })
        self.assertEqual(login_response.status_code, 200)
        print("User login OK")


    def test_logout_user(self):
        user = CustomUser.objects.create_user(
            email='test@test.de',
            username='testuser',
            password='testpassword123'
        )
        user.is_active = True
        user.save()
        self.client.post(reverse('login'), data={
            'email': 'test@test.de',
            'password': 'testpassword123'
        })
        logout_response = self.client.post(reverse('logout'))
        self.assertEqual(logout_response.status_code, 204)
        print("User logout OK")
        

class UserSendResetPasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@test.de',
            username='testuser',
            password='testpassword123'
        )
        self.user.is_active = True
        self.user.save()

    @patch('users.views.reset_password')
    def test_send_reset_email(self, mock_reset_password):
        response = self.client.post(reverse('reset_email'), data={
            'email': 'test@test.de'
        })
        self.assertEqual(response.status_code, 200)
        mock_reset_password.assert_called_once_with('test@test.de', ANY)
        print("reset email has beent sent OK")
        
        
class ResetPasswordTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@test.de',
            username='testuser',
            password='testpassword123'
        )
        self.user.is_active = True
        self.user.save()
        self.request = self.client.request().wsgi_request

    @patch('users.views.EmailMultiAlternatives.send')
    def test_reset_password(self, mock_send):
        reset_password(self.user.email, self.request)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_count, 1)
        print("Reset password email send test OK")

    @patch('users.views.EmailMultiAlternatives.send')
    def test_reset_password_user_not_found(self, mock_send):
        with self.assertRaises(CustomUser.DoesNotExist):
            reset_password('nonexistent@test.de', self.request)
        mock_send.assert_not_called()
        print("Reset password user not found test OK")
        
        
class CustomUserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@test.de',
            username='testuser',
            password='testpassword123'
        )
        self.user.is_active = True
        self.user.save()
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

    def test_get_users(self):
        response = self.client.get(reverse('user-get'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'test@test.de')
        print("customuser get method OK")

    def test_update_user_password(self):
        new_password = 'newpassword123'
        response = self.client.put(reverse('user-update', args=[self.uidb64]), data={
            'password': new_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
        print("customuser put method OK")

    def test_delete_user(self):
        response = self.client.delete(reverse('delete_user', args=[self.uidb64]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())
        print("customuser delete method OK")
        
        
class ResendActivationEmailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@test.de',
            username='testuser',
            password='testpassword123'
        )
        self.user.is_active = False
        self.user.save()

    @patch('users.views.send_activation_email')
    def test_resend_activation_email_user_not_active(self, mock_send_activation_email):
        response = self.client.post(reverse('verify_again'), data={
            'email': 'test@test.de'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Activation email resent.')
        mock_send_activation_email.assert_called_once_with(self.user, ANY)
        print("resending activation email send test OK")

    def test_resend_activation_email_user_active(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(reverse('verify_again'), data={
            'email': 'test@test.de'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User is already active.')
        print("user is already active test OK")
        

    def test_resend_activation_email_user_not_found(self):
        response = self.client.post(reverse('verify_again'), data={
            'email': 'nonexistent@test.de'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'User not found.')
        print("user not in database test OK")
        

    def test_resend_activation_email_no_email_provided(self):
        response = self.client.post(reverse('verify_again'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Email not provided.')
        print("no email test OK")
        
        
class SendActivationEmailTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@test.de',
            username='testuser',
            password='testpassword123'
        )
        self.user.is_active = False
        self.user.save()
        self.request = self.client.request().wsgi_request

    @patch('users.views.EmailMultiAlternatives.send')
    def test_send_activation_email(self, mock_send):
        send_activation_email(self.user, self.request)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_count, 1)
        print("Activation email send test OK")
        
        
class CsrfTokenTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_csrf_token(self):
        response = self.client.get(reverse('csrf_token'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('csrf_token', response.json())
        print("csrf token recieved OK")