"""
ASGI config for blockchain_explorer project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blockchain_explorer.settings')

application = get_asgi_application()