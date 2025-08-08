from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
import json

from .models import TalentEventRegistration, RegistrationActivity


class TalentEventRegistrationModelTest(TestCase):
    """Test cases for TalentEventRegistration model"""

    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'full_name': 'Test Participant',
            'gender': 'male',
            'date_of_birth': '15-08-1995',
            'age_group': '21-40',
            'event': 'singing',
            'city': 'Mumbai',
            'whatsapp_number': '+919876543210',
            'terms': 'yes'
        }

    def test_create_registration(self):
        """Test creating a registration"""
        # Create a fake image file
        photo = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        registration = TalentEventRegistration.objects.create(
            photo=photo,
            **self.valid_data
        )

        self.assertEqual(registration.full_name, 'Test Participant')
        self.assertEqual(registration.event, 'singing')
        self.assertTrue(registration.is_active)
        self.assertTrue(registration.registration_id.startswith('BK2025-'))

    def test_terms_validation(self):
        """Test that terms must be agreed to"""
        with self.assertRaises(ValueError):
            TalentEventRegistration.objects.create(
                terms='no',
                **{k: v for k, v in self.valid_data.items() if k != 'terms'}
            )

    def test_string_representation(self):
        """Test string representation of model"""
        photo = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        registration = TalentEventRegistration.objects.create(
            photo=photo,
            **self.valid_data
        )

        expected = f"{registration.full_name} - {registration.get_event_display()}"
        self.assertEqual(str(registration), expected)


class TalentEventRegistrationAPITest(APITestCase):
    """Test cases for registration API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.valid_data = {
            'full_name': 'API Test Participant',
            'gender': 'female',
            'date_of_birth': '20-05-1998',
            'age_group': '21-40',
            'event': 'dancing',
            'city': 'Delhi',
            'whatsapp_number': '9876543210',
            'terms': 'yes'
        }

    def test_create_registration_api(self):
        """Test creating registration via API"""
        # Create a fake image file
        photo = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        data = self.valid_data.copy()
        data['photo'] = photo

        url = reverse('talenteventregistration-list')
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('registration_id', response.data)

    def test_invalid_registration_api(self):
        """Test API with invalid data"""
        # Missing required fields
        invalid_data = {
            'full_name': 'Test',
            'terms': 'no'  # Terms not agreed
        }

        url = reverse('talenteventregistration-list')
        response = self.client.post(url, invalid_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_registration_statistics_api(self):
        """Test statistics API endpoint"""
        # Create some test registrations
        photo = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        TalentEventRegistration.objects.create(
            photo=photo,
            **self.valid_data
        )

        url = reverse('talenteventregistration-statistics')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_registrations', response.data)
        self.assertIn('event_statistics', response.data)

    def test_health_check(self):
        """Test health check endpoint"""
        url = reverse('health_check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')


class RegistrationActivityTest(TestCase):
    """Test cases for RegistrationActivity model"""

    def setUp(self):
        """Set up test data"""
        photo = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        self.registration = TalentEventRegistration.objects.create(
            full_name='Test Participant',
            gender='male',
            date_of_birth='15-08-1995',
            age_group='21-40',
            event='singing',
            city='Mumbai',
            whatsapp_number='+919876543210',
            photo=photo,
            terms='yes'
        )

    def test_create_activity(self):
        """Test creating registration activity"""
        activity = RegistrationActivity.objects.create(
            registration=self.registration,
            activity_type='registration',
            description='Registration submitted successfully',
            metadata={'ip_address': '127.0.0.1'}
        )

        self.assertEqual(activity.registration, self.registration)
        self.assertEqual(activity.activity_type, 'registration')
        self.assertEqual(activity.metadata['ip_address'], '127.0.0.1')

    def test_activity_string_representation(self):
        """Test string representation of activity"""
        activity = RegistrationActivity.objects.create(
            registration=self.registration,
            activity_type='registration',
            description='Test activity'
        )

        expected = f"{self.registration.full_name} - Registration Submitted"
        self.assertEqual(str(activity), expected)
