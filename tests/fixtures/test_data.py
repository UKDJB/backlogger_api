# tests/fixtures/test_data.py
"""Test data and constants used across test files."""

# User registration data
VALID_REGISTRATION_DATA = {
    'email': 'david_j_brown@outlook.com',
    'password': 'SecureTestPassword123!',
    'password_confirm': 'SecureTestPassword123!',
    'first_name': 'David',
    'last_name': 'Brown'
}

TEST_USER_EMAIL = 'david_j_brown@outlook.com'

# Template test data
TEMPLATE_TEST_CONTEXT = {
    'first_name': 'David',
    'verification_url': 'http://test.com/verify',
    'plain_email_address': 'david_j_brown@outlook.com'
}

# Add more test data sets as needed for different test scenarios
INVALID_PASSWORDS = [
    'short',                  # Too short
    'withoutspecialchar123',  # No special character
    'WITHOUT@LOWERCASE123',   # No lowercase
    'nouppercase@123',       # No uppercase
    'NoNumbers@',            # No numbers
]

INVALID_EMAILS = [
    '',                      # Empty
    'invalid-email',         # No domain
    '@nodomain.com',        # No local part
    'no@domain',            # Incomplete domain
    'spaces in@email.com',  # Contains spaces
]
