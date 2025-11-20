import os
import django

from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import the ProtocolTypeRouter application from core.routing
from .routing import application  # noqa: E402

# `application` is the ASGI app used by Daphne / Uvicorn / ASGI servers.
