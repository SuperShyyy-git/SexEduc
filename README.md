# Sex Education System

A comprehensive Django-based sex education platform with atomic design principles.

## Project Structure

```
sex_education_system/
├── accounts/              # User management
├── courses/               # Learning modules  
├── quizzes/              # Assessments
├── content_management/   # Admin content control
├── static/
│   ├── css/
│   │   ├── atoms/       # Button styles, input styles
│   │   ├── molecules/   # Form styles, card styles
│   │   └── organisms/   # Header, footer, navigation
│   ├── js/
│   │   └── main.js      # Main JavaScript functionality
│   └── images/
├── templates/
│   ├── atoms/           # Reusable button components
│   ├── molecules/       # Reusable form components
│   ├── organisms/       # Header, footer templates
│   ├── pages/           # Full page templates
│   └── base.html        # Base template
├── sex_education_system/ # Django project settings
└── manage.py
```

## Getting Started

### 1. Install Dependencies

```bash
pip install django
```

### 2. Configure Settings

Update `sex_education_system/settings.py` to add the apps to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'courses',
    'quizzes',
    'content_management',
]

# Add template and static file configurations
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # ... rest of config
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see your application.

## Atomic Design Structure

This project follows atomic design principles:

### Atoms
- **CSS**: Basic building blocks (buttons, inputs)
- **Templates**: Minimal reusable components

### Molecules  
- **CSS**: Combinations of atoms (forms, cards)
- **Templates**: Functional components built from atoms

### Organisms
- **CSS**: Complex UI sections (header, footer, navigation)
- **Templates**: Complete sections combining molecules and atoms

### Pages
- Full page layouts that combine all design levels

## Features

- 🎓 **Learning Modules**: Structured courses on sexual education
- ✅ **Assessment Quizzes**: Interactive quizzes to test knowledge
- 👥 **User Management**: Authentication and user profiles
- 🔒 **Admin Content Control**: Manage educational content
- 📱 **Responsive Design**: Mobile-friendly atomic design system
- 🎨 **Modern UI**: Gradient backgrounds, smooth animations

## Next Steps

1. Define models for each app (User profiles, Courses, Quizzes, etc.)
2. Create views and URL patterns
3. Add authentication system
4. Build out course content management
5. Implement quiz functionality
6. Add user progress tracking

## License

Educational project for comprehensive sex education.
