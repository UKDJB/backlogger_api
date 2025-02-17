# tests/unit/authentication/test_serializers.py
import pytest
from authentication.serializers import RegistrationSerializer


@pytest.mark.unit
@pytest.mark.auth
@pytest.mark.django_db
class TestRegistrationSerializer:
    """Unit tests for the RegistrationSerializer."""

    def test_valid_data(self, valid_user_data):
        """Test serializer with valid registration data."""
        serializer = RegistrationSerializer(data=valid_user_data)
        assert serializer.is_valid()
        assert set(serializer.validated_data.keys()) >= {
            'email', 'password', 'first_name', 'last_name'}

    @pytest.mark.parametrize(
        "data, expected_error",
        [
            ({'password': 'short', 'password_confirm': 'short'}, 'password'),
            ({'password': 'Withoutspecialchar123',
             'password_confirm': 'withoutspecialchar123'}, 'password'),
            ({'password': 'Testpass@123',
             'password_confirm': 'differentpass@123'}, 'password_confirm'),
        ],
    )
    def test_password_validation(self, valid_user_data, data, expected_error):
        """Test password validation rules."""
        invalid_data = {**valid_user_data, **data}
        serializer = RegistrationSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert expected_error in serializer.errors

    def test_email_validation(self, valid_user_data):
        """Test invalid email format."""
        valid_user_data["email"] = "invalid-email"
        serializer = RegistrationSerializer(data=valid_user_data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    @pytest.mark.parametrize("missing_field", ['email', 'password', 'password_confirm', 'first_name', 'last_name'])
    def test_required_fields(self, valid_user_data, missing_field):
        """Test that all required fields are enforced."""
        del valid_user_data[missing_field]
        serializer = RegistrationSerializer(data=valid_user_data)
        assert not serializer.is_valid()
        assert missing_field in serializer.errors
