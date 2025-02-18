# tests/conftest.py
import django
import os
import pytest
import sys

pytest_plugins = [
    "tests.fixtures.authentications",
    "tests.fixtures.test_data"
]

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backlogger_api.settings')
    django.setup()
