# tests/integration/authentication/test_registration.py
import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.fixtures.test_data import VALID_REGISTRATION_DATA, TEST_USER_EMAIL

User = get_user_model()


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.email
@pytest.mark.django_db
class TestRegistrationFlow:
    """Integration tests for the complete registration process."""

    def test_successful_registration(self, api_client):
        """Test successful user registration with valid data."""
        url = reverse('authentication:register')
        response = api_client.post(url, VALID_REGISTRATION_DATA, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert len(mail.outbox) == 1

        user = User.objects.first()
        assert user.email == VALID_REGISTRATION_DATA['email']
        assert not user.is_active
        assert not user.email_verified

        # Verify email content
        email = mail.outbox[0]
        assert email.to[0] == TEST_USER_EMAIL
        assert 'Please verify your email address' in email.subject
        assert 'verify-email' in email.alternatives[0][0]

    def test_registration_with_existing_email(self, api_client):
        """Test registration attempt with an already registered email."""
        # Create initial user
        User.objects.create_user(
            email=VALID_REGISTRATION_DATA['email'],
            password='oldpassword'
        )

        # Attempt registration with same email
        url = reverse('authentication:register')
        response = api_client.post(url, VALID_REGISTRATION_DATA, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert User.objects.count() == 1
        assert len(mail.outbox) == 0

    def test_registration_with_invalid_password(self, api_client):
        """Test registration with invalid password combinations."""
        invalid_data = VALID_REGISTRATION_DATA.copy()
        invalid_data['password'] = 'weak'
        invalid_data['password_confirm'] = 'weak'

        url = reverse('authentication:register')
        response = api_client.post(url, invalid_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
        assert User.objects.count() == 0
        assert len(mail.outbox) == 0

    def test_registration_with_mismatched_passwords(self, api_client):
        """Test registration with non-matching passwords."""
        mismatched_data = VALID_REGISTRATION_DATA.copy()
        mismatched_data['password_confirm'] = 'DifferentP@ssw0rd123'

        url = reverse('authentication:register')
        response = api_client.post(url, mismatched_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data
        assert User.objects.count() == 0
        assert len(mail.outbox) == 0

    def test_registration_email_template_variables(self, api_client):
        """Test that registration email contains all required template variables."""
        # Use different email to avoid conflicts
        modified_data = VALID_REGISTRATION_DATA.copy()
        modified_data['email'] = 'another.test@example.com'

        url = reverse('authentication:register')
        response = api_client.post(url, modified_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert len(mail.outbox) == 1

        email = mail.outbox[0]
        html_content = email.alternatives[0][0]

        assert modified_data['first_name'] in html_content
        formatted_email = modified_data['email'].replace('@', ' @ ')
        assert formatted_email in html_content
        assert 'verify-email' in html_content
