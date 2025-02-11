# tests/authentication/test_views.py
import pytest
from django.test import TestCase
from authentication.models import CustomUser


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email="test@example.com",
        password="testpassword"
    )
    assert user.email == "test@example.com"
    assert user.password != "testpassword"  # Password should be hashed
    assert not user.is_active
    assert not user.is_staff
