#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'talent_event_backend.settings')
    django.setup()

    print("🚀 Starting Bhudev Kalakaar 2025 Django Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000/")
    print("🔗 Admin panel: http://127.0.0.1:8000/admin/")
    print("📋 Registration form: http://127.0.0.1:8000/")
    print("✅ Confirmation page: http://127.0.0.1:8000/confirmation/")
    print("🔌 API endpoint: http://127.0.0.1:8000/api/submit/")
    print("-" * 50)

    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
