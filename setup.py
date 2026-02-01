"""
Setup script for Sex Education System
Run this to initialize the database and create a superuser
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sex_education_system.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

print("=" * 50)
print("Sex Education System - Setup")
print("=" * 50)

# Run migrations
print("\n1. Creating database tables...")
try:
    call_command('makemigrations', verbosity=1)
    call_command('migrate', verbosity=1)
    print("✓ Database tables created successfully!")
except Exception as e:
    print(f"✗ Error creating tables: {e}")

# Create superuser if it doesn't exist
print("\n2. Creating superuser account...")
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Superuser created!")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("✓ Superuser already exists")
except Exception as e:
    print(f"✗ Error creating superuser: {e}")

print("\n" + "=" * 50)
print("Setup Complete!")
print("=" * 50)
print("\nTo run the development server:")
print("  python manage.py runserver")
print("\nThen visit: http://127.0.0.1:8000/")
print("Admin panel: http://127.0.0.1:8000/admin/")
