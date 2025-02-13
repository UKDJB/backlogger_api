# backlogger_api/settings/__init__.py

from .base import *

# Use development settings by default, if present
try:
    from .development import *
except ImportError:
    pass

# Use production settings if DJANGO_ENV is set to 'production'
if os.getenv('DJANGO_ENV') == 'production':
    try:
        from .production import *
    except ImportError:
        pass
