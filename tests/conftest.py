# src/tests/conftest.py
import pytest
from django.core import mail
import django
from django.conf import settings
import os


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backlogger.settings')
    django.setup()


@pytest.fixture(autouse=True)
def email_outbox():
    """Clear the email outbox before each test"""
    mail.outbox = []


@pytest.fixture
def valid_user_data():
    """Provide valid user registration data for tests"""
    return {
        'email': 'test@example.com',
        'password': 'StrongPass123!',
        'password_confirm': 'StrongPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def registered_user(django_user_model, valid_user_data):
    """Create and return a registered user"""
    user_data = valid_user_data.copy()
    password = user_data.pop('password')
    user_data.pop('password_confirm', None)  # Remove if exists
    user = django_user_model.objects.create_user(
        password=password,
        **user_data
    )
    return user


@pytest.fixture
def auth_client(client, registered_user):
    """Returns an authenticated client"""
    client.force_login(registered_user)
    return client


@pytest.fixture
def api_client():
    """Returns a DRF API client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, registered_user):
    """Returns an authenticated DRF API client"""
    api_client.force_authenticate(user=registered_user)
    return api_client
