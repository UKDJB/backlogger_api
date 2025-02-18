# tests/fixtures/authentications.py
"""Authentications related test fixtures."""
import pytest
from django.core import mail
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """Returns a DRF API client."""
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, registered_user):
    """Returns an authenticated DRF API client."""
    api_client.force_authenticate(user=registered_user)
    return api_client


@pytest.fixture(autouse=True)
def clear_mail_outbox():
    """Clear the mail outbox before each test."""
    mail.outbox = []


@pytest.fixture
def registered_user(django_user_model, valid_user_data):
    """Create and return a registered user."""
    user_data = valid_user_data.copy()
    password = user_data.pop('password')
    user_data.pop('password_confirm', None)  # Remove if exists
    user = django_user_model.objects.create_user(
        password=password,
        **user_data
    )
    return user


@pytest.fixture
def template_context():
    """Fixture providing standard template context."""
    return {
        'first_name': 'David',
        'verification_url': 'http://test.com/verify',
        'plain_email_address': 'david_j_brown@outlook.com'
    }


@pytest.fixture
def unverified_user(django_user_model):
    """Create an unverified user for testing."""
    return django_user_model.objects.create_user(
        email='test@example.com',
        password='testpass123',
        is_active=False,
        email_verified=False
    )


@pytest.fixture
def valid_user_data():
    """Provide valid user registration data for tests."""
    return {
        'email': 'test@example.com',
        'password': 'StrongPass123!',
        'password_confirm': 'StrongPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }
