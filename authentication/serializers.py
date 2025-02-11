# authentication/serializers.py
from django.contrib.auth import get_user_model, password_validation
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            validators.EmailValidator(message="Enter a valid email address.")
        ]
    )
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirm',
                  'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):

        # Custom email validation - check if email already exists
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email address is already in use.")
        return value.lower()

    def validate_password(self, value):
        # Validate password using Django's password validators
        try:
            # This will use all validators from AUTH_PASSWORD_VALIDATORS
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        # Check that the passwords match and apply any business rules
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Passwords don't match."
            })

        # Example of a business rule: domain restriction
        email_domain = data['email'].split('@')[1]
        allowed_domains = ['example.com', 'backlogger.io']
        if email_domain not in allowed_domains:
            raise serializers.ValidationError({
                'email': f"Email must be from one of these domains: {', '.join(allowed_domains)}"
            })

        return data

    def create(self, validated_data):
        # Remove password_confirm from the data
        validated_data.pop('password_confirm')

        # Create the user using the custom manager
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        return user


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'is_active', 'email_verified')
        read_only_fields = ('is_active', 'email_verified')
