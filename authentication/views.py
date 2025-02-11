# authentication/views.py
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .serializers import RegistrationSerializer, UserSerializer
from .utils import send_verification_email
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class RegistrationView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    @method_decorator(ratelimit(key='ip', rate='5/m', method=['POST']))
    def post(self, request):
        # Register a new user and send verification email.
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                # Create inactive user
                user = serializer.save(is_active=False)

                # Generate verification URL
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # Build verification URL
                verification_url = f"{request.build_absolute_uri(
                    '/').rstrip('/')}/verify-email/{uid}/{token}"

                # Send verification email
                try:
                    send_verification_email(user, verification_url)
                except Exception as e:
                    logger.error(
                        f"Failed to send verification email: {str(e)}")
                    user.delete()  # Rollback user creation if email fails
                    return Response(
                        {'error': 'Failed to send verification email'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                return Response({
                    'message': 'Registration successful. Please check your email to verify your account.',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {'error': 'An unexpected error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmailVerificationView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        # Verify user's email address.
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                if user.email_verified:
                    return Response({
                        'message': 'Email was already verified'
                    }, status=status.HTTP_200_OK)

                user.email_verified = True
                user.is_active = True
                user.save()

                return Response({
                    'message': 'Email successfully verified'
                }, status=status.HTTP_200_OK)

            return Response({
                'error': 'Invalid verification token'
            }, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Invalid verification link'
            }, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(views.APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method=['POST']))
    def post(self, request):
        # Check if email is available and valid.
        email = request.data.get('email', '').lower()

        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use Django's email validator
            django_validate_email(email)

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({
                    'error': 'This email address is already registered'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Email is available'
            }, status=status.HTTP_200_OK)

        except ValidationError:
            return Response({
                'error': 'Enter a valid email address'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordCheckView(views.APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method=['POST']))
    def post(self, request):
        # Check if password meets requirements.
        password = request.data.get('password', '')

        if not password:
            return Response({
                'error': 'Password is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use Django's password validation utility
            password_validation.validate_password(password)
            return Response({
                'message': 'Password meets requirements'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'error': e.messages[0] if e.messages else 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)
