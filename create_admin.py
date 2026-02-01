"""
One-time script to create admin user on Render
Run this after deployment to create your first admin account
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sex_education_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment variables
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('ADMIN_PASSWORD', 'changeme123')

# Create admin user if it doesn't exist
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Superuser '{username}' created successfully!")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
