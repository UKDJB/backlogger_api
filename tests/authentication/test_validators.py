# tests/authentication/test_validators.py
import pytest
from django.core.exceptions import ValidationError
from authentication.validators import (
    SpecialCharacterValidator,
    UppercaseValidator,
    LowercaseValidator,
    NumberValidator,
    RepeatedCharacterValidator,
    NoUserInfoValidator,
    MaxLengthValidator
)


@pytest.mark.django_db
class TestPasswordValidators:
    def test_special_character_validator(self):
        validator = SpecialCharacterValidator()

        # Should pass
        validator.validate('Test@123')

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate('TestPass123')

    def test_uppercase_validator(self):
        validator = UppercaseValidator()

        # Should pass
        validator.validate('Test123')

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate('test123')

    def test_lowercase_validator(self):
        validator = LowercaseValidator()

        # Should pass
        validator.validate('Test123')

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate('TEST123')

    def test_number_validator(self):
        validator = NumberValidator()

        # Should pass
        validator.validate('Test123')

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate('TestPass')

    def test_repeated_character_validator(self):
        validator = RepeatedCharacterValidator(max_repeats=2)

        # Should pass
        validator.validate('Test123')

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate('Tesssst123')

    def test_max_length_validator(self):
        validator = MaxLengthValidator(max_length=10)

        # Should pass
        validator.validate('Test123')

        # Should fail
        with pytest.raises(ValidationError):
            validator.validate('TestPass123456789')
