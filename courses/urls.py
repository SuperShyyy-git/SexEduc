from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Public views
    path('', views.course_list_view, name='list'),
    path('<int:course_id>/', views.course_detail_view, name='detail'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.lesson_view, name='lesson'),
    path('<int:course_id>/lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_complete'),
    
    # Content management views (staff only)
    path('create/', views.create_course, name='create'),
    path('<int:course_id>/edit/', views.edit_course, name='edit'),
    path('<int:course_id>/delete/', views.delete_course, name='delete'),
    path('<int:course_id>/archive/', views.archive_course, name='archive'),
    path('<int:course_id>/restore/', views.restore_course, name='restore'),
    path('archived/', views.archived_courses_view, name='archived'),
    path('lesson/create/', views.create_lesson, name='create_lesson'),
    path('lesson/create/<int:course_id>/', views.create_lesson, name='create_lesson_for_course'),
    path('lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    
    # Diagnostic tools (staff only)
    path('video-diagnostic/', views.video_diagnostic_view, name='video_diagnostic'),
]
