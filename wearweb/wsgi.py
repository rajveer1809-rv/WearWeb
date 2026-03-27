"""
WSGI config for wearweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wearweb.settings')

try:
    logger.info("Initializing WSGI application...")
    application = get_wsgi_application()
    logger.info("WSGI application initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize WSGI application: {e}", exc_info=True)
    raise
