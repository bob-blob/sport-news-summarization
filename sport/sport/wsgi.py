"""
WSGI config for NewsSummarizationSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/opt/bitnami/apps/django/django_projects/news')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsSummarizationSystem.settings")

application = get_wsgi_application()