"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application

# Auto-create superuser on first boot (safe: skips if already exists)
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@taskpulse.com', 'admin123')
        print('[TaskPulse] Superuser "admin" created successfully.')
    else:
        print('[TaskPulse] Superuser "admin" already exists.')
except Exception as e:
    print(f'[TaskPulse] Superuser creation skipped: {e}')

