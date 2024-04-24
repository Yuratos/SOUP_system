import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soup_system_settings.settings')

application = get_wsgi_application()
