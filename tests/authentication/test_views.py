# tests/test_authentication/test_views.py
from authentication.serializers import RegistrationSerializer
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_user_data():
    return {
        'email': 'test@example.com',
        'password': 'SecureP@ssw0rd123',
        'password_confirm': 'SecureP@ssw0rd123',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.mark.django_db
class TestRegistrationView:
    def test_successful_registration(self, api_client, valid_user_data):
        # Test successful user registration with valid data
        url = reverse('authentication:register')
        response = api_client.post(url, valid_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert len(mail.outbox) == 1  # Verify email was sent

        user = User.objects.first()
        assert user.email == valid_user_data['email']
        assert not user.is_active  # User should be inactive until email verification
        assert not user.email_verified

    def test_registration_with_existing_email(self, api_client, valid_user_data):
        # Test registration attempt with already registered email
        # Create a user first
        User.objects.create_user(
            email=valid_user_data['email'], password='oldpassword')

        url = reverse('authentication:register')
        response = api_client.post(url, valid_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert User.objects.count() == 1  # No new user should be created

    def test_registration_with_invalid_password(self, api_client, valid_user_data):
        # Test registration with weak password
        valid_user_data['password'] = 'weak'
        valid_user_data['password_confirm'] = 'weak'

        url = reverse('authentication:register')
        response = api_client.post(url, valid_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
        assert User.objects.count() == 0

    def test_registration_with_mismatched_passwords(self, api_client, valid_user_data):
        # Test registration with non-matching passwords
        valid_user_data['password_confirm'] = 'DifferentP@ssw0rd123'

        url = reverse('authentication:register')
        response = api_client.post(url, valid_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data
        assert User.objects.count() == 0


@pytest.mark.django_db
class TestEmailVerificationView:
    def test_successful_verification(self, api_client):
        # Test successful email verification
        # Create an unverified user
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=False
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse('authentication:verify-email',
                      kwargs={'uidb64': uid, 'token': token})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Refresh user from database
        user.refresh_from_db()
        assert user.is_active
        assert user.email_verified

    def test_invalid_verification_link(self, api_client):
        # Test verification with invalid token
        url = reverse('authentication:verify-email', kwargs={
            'uidb64': 'invalid-uid',
            'token': 'invalid-token'
        })
        response = api_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEmailCheckView:
    def test_valid_email_format(self, api_client):
        url = reverse('authentication:check-email')
        response = api_client.post(url, {'email': 'test@example.com'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Email is available'

    def test_invalid_email_format(self, api_client):
        url = reverse('authentication:check-email')
        response = api_client.post(url, {'email': 'invalid-email'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_empty_email(self, api_client):
        url = reverse('authentication:check-email')
        response = api_client.post(url, {'email': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Email is required'

    def test_existing_email(self, api_client, django_user_model):
        # Create a user first
        existing_email = 'existing@example.com'
        django_user_model.objects.create_user(
            email=existing_email,
            password='TestPass123!'
        )

        url = reverse('authentication:check-email')
        response = api_client.post(url, {'email': existing_email})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'This email address is already registered'


@pytest.mark.django_db
class TestPasswordCheckView:
    def test_valid_password(self, api_client):
        # Test checking a valid password
        url = reverse('authentication:check-password')
        response = api_client.post(url, {'password': 'SecureP@ssw0rd123'})

        assert response.status_code == status.HTTP_200_OK

    def test_weak_password(self, api_client):
        # Test checking a weak password
        url = reverse('authentication:check-password')
        response = api_client.post(url, {'password': 'weak'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPasswordCheckView:
    def test_password_with_all_requirements(self, api_client):
        url = reverse('authentication:check-password')
        response = api_client.post(url, {
            'password': 'Test@123Pass'
        })
        assert response.status_code == status.HTTP_200_OK

    def test_password_missing_special_char(self, api_client):
        url = reverse('authentication:check-password')
        response = api_client.post(url, {
            'password': 'TestPass123'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_missing_number(self, api_client):
        url = reverse('authentication:check-password')
        response = api_client.post(url, {
            'password': 'Test@Pass'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short(self, api_client):
        url = reverse('authentication:check-password')
        response = api_client.post(url, {
            'password': 'T@1'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEmailCheckView:
    def test_valid_email_format(self, api_client):
        url = reverse('authentication:check-email')
        response = api_client.post(url, {
            'email': 'test@example.com'
        })
        assert response.status_code == status.HTTP_200_OK

    def test_invalid_email_format(self, api_client):
        url = reverse('authentication:check-email')
        response = api_client.post(url, {
            'email': 'invalid-email'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_email(self, api_client):
        url = reverse('authentication:check-email')
        response = api_client.post(url, {
            'email': ''
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_existing_email(self, api_client, django_user_model):
        # Create a user first
        django_user_model.objects.create_user(
            email='existing@example.com',
            password='TestPass123'
        )

        url = reverse('authentication:check-email')
        response = api_client.post(url, {
            'email': 'existing@example.com'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
