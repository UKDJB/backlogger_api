# apps/authentication/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class SpecialCharacterValidator:
    # Validate that the password contains special characters.
    def __init__(self, min_special_chars=1):
        self.min_special_chars = min_special_chars
        self.special_pattern = r'[!@#$%^&*(),.?":{}|<>]'

    def validate(self, password, user=None):
        special_chars = re.findall(self.special_pattern, password)
        if len(special_chars) < self.min_special_chars:
            raise ValidationError(
                _(f'Password must contain at least {
                  self.min_special_chars} special character(s).'),
                code='password_no_special',
                params={'min_special_chars': self.min_special_chars},
            )

    def get_help_text(self):
        return _(f'Your password must contain at least {self.min_special_chars} special character(s).')


class UppercaseValidator:
    # Validate that the password contains uppercase characters.
    def __init__(self, min_uppercase=1):
        self.min_uppercase = min_uppercase

    def validate(self, password, user=None):
        uppercase_chars = re.findall(r'[A-Z]', password)
        if len(uppercase_chars) < self.min_uppercase:
            raise ValidationError(
                _(f'Password must contain at least {
                  self.min_uppercase} uppercase letter(s).'),
                code='password_no_uppercase',
                params={'min_uppercase': self.min_uppercase},
            )

    def get_help_text(self):
        return _(f'Your password must contain at least {self.min_uppercase} uppercase letter(s).')


class LowercaseValidator:
    # Validate that the password contains lowercase characters.
    def __init__(self, min_lowercase=1):
        self.min_lowercase = min_lowercase

    def validate(self, password, user=None):
        lowercase_chars = re.findall(r'[a-z]', password)
        if len(lowercase_chars) < self.min_lowercase:
            raise ValidationError(
                _(f'Password must contain at least {
                  self.min_lowercase} lowercase letter(s).'),
                code='password_no_lowercase',
                params={'min_lowercase': self.min_lowercase},
            )

    def get_help_text(self):
        return _(f'Your password must contain at least {self.min_lowercase} lowercase letter(s).')


class NumberValidator:
    # Validate that the password contains numbers.
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        digits = re.findall(r'[0-9]', password)
        if len(digits) < self.min_digits:
            raise ValidationError(
                _(f'Password must contain at least {
                  self.min_digits} number(s).'),
                code='password_no_numbers',
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return _(f'Your password must contain at least {self.min_digits} number(s).')


class RepeatedCharacterValidator:
    # Validate that the password doesn't contain too many repeated characters.
    def __init__(self, max_repeats=3):
        self.max_repeats = max_repeats

    def validate(self, password, user=None):
        if re.search(r'(.)\1{' + str(self.max_repeats) + ',}', password):
            raise ValidationError(
                _(f'Password cannot contain more than {
                  self.max_repeats} repeated characters in a row.'),
                code='password_repeated_characters',
                params={'max_repeats': self.max_repeats},
            )

    def get_help_text(self):
        return _(f'Your password cannot contain more than {self.max_repeats} repeated characters in a row.')


class NoUserInfoValidator:
    # Validate that the password doesn't contain user information.
    # More specific than Django's UserAttributeSimilarityValidator.
    def validate(self, password, user=None):
        if not user:
            return

        # List of user attributes to check
        user_attrs = ['email', 'first_name', 'last_name']

        for attribute in user_attrs:
            value = getattr(user, attribute, None)
            if not value:
                continue

            value = value.lower()
            password_lower = password.lower()

            # Check if any part of the attribute (3 or more chars) is in the password
            for i in range(len(value) - 2):
                if value[i:i + 3] in password_lower:
                    raise ValidationError(
                        _('Password cannot contain parts of your personal information.'),
                        code='password_contains_user_info',
                    )

    def get_help_text(self):
        return _('Your password cannot contain parts of your personal information.')


class MaxLengthValidator:
    # Validate that the password isn't too long (prevent DOS attacks).
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _(f'Password must be no more than {
                  self.max_length} characters.'),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _(f'Your password must be no more than {self.max_length} characters.')
