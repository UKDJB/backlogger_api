# tests/integration/authentications/test_validation.py
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.email
@pytest.mark.django_db
class TestEmailValidation:
    """Integration tests for email validation endpoints."""

    def test_valid_email_format(self, api_client):
        """Test checking a valid email format."""
        url = reverse('authentications:check-email')
        response = api_client.post(
            url, {'email': 'test@example.com'}, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Email is available'

    def test_invalid_email_format(self, api_client):
        """Test checking an invalid email format."""
        url = reverse('authentications:check-email')
        response = api_client.post(
            url, {'email': 'invalid-email'}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_empty_email(self, api_client):
        """Test checking an empty email."""
        url = reverse('authentications:check-email')
        response = api_client.post(url, {'email': ''}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Email is required'

    def test_existing_email(self, api_client):
        """Test checking an already registered email."""
        # Create a user first
        User.objects.create_user(
            email='existing@example.com',
            password='TestPass123'
        )

        url = reverse('authentications:check-email')
        response = api_client.post(
            url, {'email': 'existing@example.com'}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'This email address is already registered'


@pytest.mark.integration
@pytest.mark.auth
class TestPasswordValidation:
    """Integration tests for password validation endpoints."""

    def test_valid_password(self, api_client):
        """Test checking a valid password."""
        url = reverse('authentications:check-password')
        response = api_client.post(url, {
            'password': 'Test@123Pass'
        }, format='json')

        assert response.status_code == status.HTTP_200_OK

    def test_password_missing_special_char(self, api_client):
        """Test checking a password without special characters."""
        url = reverse('authentications:check-password')
        response = api_client.post(url, {
            'password': 'TestPass123'
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_missing_number(self, api_client):
        """Test checking a password without numbers."""
        url = reverse('authentications:check-password')
        response = api_client.post(url, {
            'password': 'Test@Pass'
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short(self, api_client):
        """Test checking a password that's too short."""
        url = reverse('authentications:check-password')
        response = api_client.post(url, {
            'password': 'T@1'
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_with_repeating_chars(self, api_client):
        """Test checking a password with repeating characters."""
        url = reverse('authentications:check-password')
        response = api_client.post(url, {
            'password': 'Tesssst@123'
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
