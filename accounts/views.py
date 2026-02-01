from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from courses.models import UserCourseProgress
from quizzes.models import UserQuizAttempt


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'pages/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'accounts:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'pages/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """View and edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'pages/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    """User dashboard with progress overview"""
    user = request.user
    
    # Get user progress
    course_progress = UserCourseProgress.objects.filter(user=user).select_related('course')
    quiz_attempts = UserQuizAttempt.objects.filter(user=user).select_related('quiz').order_by('-attempted_at')[:5]
    
    # Calculate statistics
    total_courses = course_progress.count()
    completed_courses = course_progress.filter(completed=True).count()
    total_quizzes = quiz_attempts.count()
    
    # Calculate average quiz score
    if total_quizzes > 0:
        avg_score = sum(attempt.score for attempt in quiz_attempts) / total_quizzes
    else:
        avg_score = 0
    
    context = {
        'course_progress': course_progress,
        'quiz_attempts': quiz_attempts,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 1),
    }
    
    return render(request, 'pages/dashboard.html', context)
