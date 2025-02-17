# tests/fixtures/factories.py
"""Test factories for generating test data."""
import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for generating test users."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Sequence(lambda n: f'First{n}')
    last_name = factory.Sequence(lambda n: f'Last{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123!')
    is_active = True
    email_verified = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to handle custom user creation."""
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
