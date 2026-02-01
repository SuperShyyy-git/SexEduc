from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from courses.models import Course, Lesson
from quizzes.models import Quiz, Question
from accounts.models import UserProfile
from django.contrib.auth.models import User


@staff_member_required
def dashboard_view(request):
    """Admin dashboard with statistics"""
    # Get statistics
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    
    # Recent users
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Recent courses
    recent_courses = Course.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'recent_users': recent_users,
        'recent_courses': recent_courses,
    }
    
    return render(request, 'pages/content_dashboard.html', context)
