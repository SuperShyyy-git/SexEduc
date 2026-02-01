# Sex Education System - Quick Start Guide

## Prerequisites
```bash
pip install Django Pillow
```

## Option 1: Automated Setup (Recommended)
Run the batch file (Windows):
```bash
run.bat
```

## Option 2: Manual Setup

### Step 1: Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Admin User
```bash
python manage.py createsuperuser
```
Follow the prompts to create username and password.

### Step 3: Run Development Server
```bash
python manage.py runserver
```

### Step 4: Access the Application
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- Courses: http://127.0.0.1:8000/courses/
- Quizzes: http://127.0.0.1:8000/quizzes/
- Register: http://127.0.0.1:8000/accounts/register/
- Login: http://127.0.0.1:8000/accounts/login/

## Quick Test
1. Go to http://127.0.0.1:8000/accounts/register/ 
2. Create a user account
3. Login and explore the dashboard
4. Visit /admin/ to add courses, lessons, and quizzes

## Troubleshooting

### If you get migration errors:
```bash
python manage.py migrate --run-syncdb
```

### To reset database:
```bash
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Features
-  User authentication (register, login, dashboard, profile)
- 📚 Course management with lessons and progress tracking
- 📝 Quizzes with answers and scoring system
- 👨‍💼 Admin content management dashboard
- 🎨 Modern, responsive UI with atomic design
