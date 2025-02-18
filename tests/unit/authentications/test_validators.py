# tests/unit/authentications/test_validators.py
import pytest
from authentications.validators import (
    SpecialCharacterValidator,
    UppercaseValidator,
    LowercaseValidator,
    NumberValidator,
    RepeatedCharacterValidator,
    MaxLengthValidator
)
from django.core.exceptions import ValidationError


@pytest.mark.unit
@pytest.mark.auth
class TestPasswordValidators:
    """Unit tests for password validation rules."""

    def test_special_character_validator(self):
        """Test password contains at least one special character."""
        validator = SpecialCharacterValidator()

        # Should pass
        validator.validate("Test@123")

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate("Test123")

    def test_uppercase_validator(self):
        """Test password contains at least one uppercase letter."""
        validator = UppercaseValidator()

        # Should pass
        validator.validate("Test@123")

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate("test@123")

    def test_lowercase_validator(self):
        """Test password contains at least one lowercase letter."""
        validator = LowercaseValidator()

        # Should pass
        validator.validate("Test@123")

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate("TEST@123")

    def test_number_validator(self):
        """Test password contains at least one number."""
        validator = NumberValidator()

        # Should pass
        validator.validate("Test@123")

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate("Test@abc")

    def test_repeated_character_validator(self):
        """Test password doesn't contain repeated characters."""
        validator = RepeatedCharacterValidator(max_repeats=2)

        # Should pass
        validator.validate("Test@123")

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate("Tesst@123")

    def test_max_length_validator(self):
        """Test password doesn't exceed maximum length."""
        validator = MaxLengthValidator(max_length=128)

        # Should pass
        validator.validate("Test@123")

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate("T" * 129)

    def test_validator_help_text(self):
        """Test that validators provide helpful error messages."""
        validators = [
            SpecialCharacterValidator(),
            UppercaseValidator(),
            LowercaseValidator(),
            NumberValidator(),
            RepeatedCharacterValidator(),
            MaxLengthValidator()
        ]

        for validator in validators:
            assert isinstance(validator.get_help_text(), str)
            assert len(validator.get_help_text()) > 0
