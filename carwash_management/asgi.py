"""
ASGI config for carwash_management project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carwash_management.settings')

application = get_asgi_application()
