from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_verification_email(user, verification_url):
    """
    Send an email verification link to the user.

    Args:
        user: The user object
        verification_url: The URL for email verification
    """
    subject = 'Verify your email address'
    html_message = f"""
    <p>Hi {user.first_name},</p>
    <p>Please click the link below to verify your email address:</p>
    <p><a href="{verification_url}">Verify Email</a></p>
    <p>If you didn't create this account, you can safely ignore this email.</p>
    <p>Thanks,<br>The Backlogger Team</p>
    """
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
