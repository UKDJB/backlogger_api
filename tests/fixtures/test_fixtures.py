# tests/fixtures/test_fixtures.py
import pytest


def test_fixture_discovery(template_context):
    """Simple test to help pytest discover fixtures."""
    assert template_context is not None
    assert 'first_name' in template_context
    assert 'verification_url' in template_context
    assert 'plain_email_address' in template_context
