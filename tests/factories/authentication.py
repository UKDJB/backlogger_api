# tests/factories/authentication.py
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
    # Add default password here instead of using PostGenerationMethodCall
    password = 'testpass123!'
    is_active = True
    email_verified = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to handle custom user creation."""
        manager = cls._get_manager(model_class)
        # If password not in kwargs, use the default one
        if 'password' not in kwargs:
            kwargs['password'] = cls.password
        return manager.create_user(*args, **kwargs)
