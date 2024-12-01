from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, VerificationCode

class ReferralTests(APITestCase):
    def test_phone_auth(self):
        url = reverse('auth')
        data = {'phone_number': '+79151230011'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data)

    def test_verify_code(self):
        user = User.objects.create(phone_number='+79151230011')
        code = VerificationCode.objects.create(user=user, code='1234')
        url = reverse('verify')
        data = {'phone_number': '+79151230011', 'code': '1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(VerificationCode.objects.get(code='1234').is_used)

    def test_user_profile_get(self):
        user = User.objects.create(phone_number='+79151230011')
        url = reverse('profile')
        response = self.client.get(url, {'phone_number': '+79151230011'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '+79151230011')