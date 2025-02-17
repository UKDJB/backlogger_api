# tests/integration/authentication/test_verification.py
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.email
@pytest.mark.django_db
class TestEmailVerificationFlow:
    """Integration tests for the email verification process."""

    def test_successful_verification(self, api_client, unverified_user):
        """Test successful email verification with a valid token."""
        uid = urlsafe_base64_encode(force_bytes(unverified_user.pk))
        token = default_token_generator.make_token(unverified_user)

        response = api_client.get(
            reverse('authentication:verify-email',
                    kwargs={'uidb64': uid, 'token': token})
        )

        assert response.status_code == status.HTTP_200_OK

        # Refresh user from DB and check verification status
        unverified_user.refresh_from_db()
        assert unverified_user.is_active
        assert unverified_user.email_verified

    @pytest.mark.parametrize(
        "uid, token, expected_status",
        [
            ("invalid-uid", "invalid-token", status.HTTP_400_BAD_REQUEST),
            (None, "invalid-token", status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_invalid_verification_link(self, api_client, uid, token, unverified_user, expected_status):
        """Test verification with an invalid or malformed token."""
        uid = uid or urlsafe_base64_encode(force_bytes(unverified_user.pk))

        response = api_client.get(
            reverse('authentication:verify-email',
                    kwargs={'uidb64': uid, 'token': token})
        )

        assert response.status_code == expected_status

    def test_expired_verification_link(self, api_client, unverified_user):
        """Test verification with an expired token after password reset."""
        uid = urlsafe_base64_encode(force_bytes(unverified_user.pk))

        # Generate a valid token BEFORE password reset
        token = default_token_generator.make_token(unverified_user)

        # Simulate token expiration by changing the password
        unverified_user.set_password('newpassword123')
        unverified_user.save()

        # Refresh the user instance to reflect database changes
        unverified_user.refresh_from_db()

        # Use the old token (should now be invalid)
        response = api_client.get(
            reverse('authentication:verify-email',
                    kwargs={'uidb64': uid, 'token': token})
        )

        # Ensure the token is now invalid
        assert response.status_code == status.HTTP_400_BAD_REQUEST, f"Expected 400, got {response.status_code}"

        # Verify user is still unverified
        unverified_user.refresh_from_db()
        assert not unverified_user.is_active
        assert not unverified_user.email_verified

    def test_already_verified_user(self, api_client, unverified_user):
        """Test verification attempt for an already verified user."""
        uid = urlsafe_base64_encode(force_bytes(unverified_user.pk))
        token = default_token_generator.make_token(unverified_user)

        # First verification
        api_client.get(reverse('authentication:verify-email',
                       kwargs={'uidb64': uid, 'token': token}))

        # Second verification attempt
        response = api_client.get(
            reverse('authentication:verify-email', kwargs={'uidb64': uid, 'token': token}))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verification_wrong_user(self, api_client, unverified_user):
        """Test using a valid token with a different user's ID."""
        token = default_token_generator.make_token(unverified_user)

        # Create a second user
        user2 = User.objects.create_user(
            email='test2@example.com', password='testpass123', is_active=False)

        # Try to verify user2 using user1's token
        uid = urlsafe_base64_encode(force_bytes(user2.pk))
        response = api_client.get(
            reverse('authentication:verify-email', kwargs={'uidb64': uid, 'token': token}))

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Ensure both users remain unverified
        user2.refresh_from_db()
        unverified_user.refresh_from_db()
        assert not user2.is_active
        assert not unverified_user.is_active
