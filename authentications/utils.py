# authentications/utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_verification_email(user, verification_url):
    """
    Send an email verification link to the user.
    """
    # Format the plain email address with spaces around @ for anti-spam
    plain_email_address = 'This message was sent to ' + \
        user.email.replace('@', ' @ ')

    context = {
        'first_name': user.first_name,
        'verification_url': verification_url,
        'email_address': user.email,
        'plain_email_address': plain_email_address,
    }

    # Create email content
    subject = "Please verify your email address"
    html_message = render_to_string(
        'authentications/activation.html', context)
    plain_message = strip_tags(html_message)

    # Create the email message
    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=None,
        to=[user.email],
    )

    # Attach HTML version
    message.attach_alternative(html_message, "text/html")

    # Send the email
    message.send(fail_silently=False)
