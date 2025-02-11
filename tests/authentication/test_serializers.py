# tests/authentication/test_serializers.py

from django.contrib.auth import get_user_model
from authentication.serializers import RegistrationSerializer
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestRegistrationSerializer:
    def test_valid_data(self, valid_user_data):
        # Test serializer with valid data
        serializer = RegistrationSerializer(data=valid_user_data)
        assert serializer.is_valid()
        user = serializer.save()

        assert user.email == valid_user_data['email']
        assert user.first_name == valid_user_data['first_name']
        assert user.last_name == valid_user_data['last_name']
        assert user.check_password(valid_user_data['password'])

    def test_password_validation(self):
        # Test password validation in serializer
        invalid_data = {
            'email': 'test@example.com',
            'password': 'weak',
            'password_confirm': 'weak',
            'first_name': 'Test',
            'last_name': 'User'
        }

        serializer = RegistrationSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
