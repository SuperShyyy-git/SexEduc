from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    # Public views
    path('', views.quiz_list_view, name='list'),
    path('<int:quiz_id>/', views.quiz_detail_view, name='detail'),
    path('<int:quiz_id>/take/', views.take_quiz_view, name='take'),
    path('<int:quiz_id>/submit/', views.take_quiz_view, name='submit'),
    path('<int:quiz_id>/results/<int:attempt_id>/', views.quiz_results_view, name='results'),
    
    # Quiz management (staff only)
    path('create/', views.create_quiz, name='create'),
    path('archive/', views.archived_quizzes_view, name='archive'),
    path('<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('<int:quiz_id>/restore/', views.restore_quiz, name='restore_quiz'),
    path('<int:quiz_id>/delete-permanent/', views.permanent_delete_quiz, name='delete_permanent'),
    
    # Question management (staff only)
    path('<int:quiz_id>/question/create/', views.create_question, name='create_question'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    # Answer management (staff only)
    path('question/<int:question_id>/answer/create/', views.create_answer, name='create_answer'),
    path('answer/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
]
