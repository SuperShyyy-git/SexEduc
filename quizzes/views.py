from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, Question, Answer, UserQuizAttempt
from .forms import QuizForm, QuestionForm, AnswerForm, AnswerFormSet
from courses.models import Course


@login_required
def quiz_list_view(request):
    """Display all active quizzes"""
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'pages/quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_detail_view(request, quiz_id):
    """Display quiz details"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    # Check if user has taken this quiz
    user_attempts = None
    if request.user.is_authenticated:
        user_attempts = UserQuizAttempt.objects.filter(
            user=request.user, 
            quiz=quiz
        ).order_by('-attempted_at')
    
    context = {
        'quiz': quiz,
        'questions_count': questions.count(),
        'user_attempts': user_attempts,
    }
    return render(request, 'pages/quiz_detail.html', context)


@login_required
def take_quiz_view(request, quiz_id):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    # Check if user has already taken this quiz
    existing_attempt = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).exists()
    if existing_attempt:
        messages.warning(request, "You have already completed this quiz. Only one attempt is allowed.")
        return redirect('quizzes:detail', quiz_id=quiz.id)
    
    if request.method == 'POST':
        # Process quiz submission
        correct_count = 0
        total_questions = questions.count()
        user_answers = {}
        
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                user_answers[str(question.id)] = answer_id
                answer = Answer.objects.filter(id=answer_id, question=question, is_correct=True).first()
                if answer:
                    correct_count += 1
        
        # Calculate score
        score = round((correct_count / total_questions) * 100) if total_questions > 0 else 0
        
        # Save attempt
        attempt = UserQuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            answers=user_answers
        )
        
        return redirect('quizzes:results', quiz_id=quiz_id, attempt_id=attempt.id)
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'pages/take_quiz.html', context)


@login_required
def quiz_results_view(request, quiz_id, attempt_id):
    """Display quiz results"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user, quiz=quiz)
    
    # Reconstruct results for review
    results = []
    user_answers = attempt.answers
    
    for question in quiz.questions.all():
        user_answer_id = user_answers.get(str(question.id))
        user_answer = Answer.objects.filter(id=user_answer_id).first() if user_answer_id else None
        correct_answer = question.correct_answer
        
        results.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': user_answer == correct_answer if user_answer else False
        })
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'results': results,
    }
    return render(request, 'pages/quiz_results.html', context)


# Content Management Views

@staff_member_required
def create_quiz(request):
    """Create a new quiz (staff only)"""
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, f'Quiz "{quiz.title}" created successfully!')
            return redirect('quizzes:edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'pages/quiz_form.html', {
        'form': form,
        'title': 'Create New Quiz',
        'submit_text': 'Create Quiz',
    })


@staff_member_required
def edit_quiz(request, quiz_id):
    """Edit an existing quiz (staff only)"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, f'Quiz "{quiz.title}" updated successfully!')
            return redirect('quizzes:edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)
    
    # Get questions for this quiz
    questions = quiz.questions.all()
    
    return render(request, 'pages/quiz_form.html', {
        'form': form,
        'quiz': quiz,
        'questions': questions,
        'title': f'Edit Quiz: {quiz.title}',
        'submit_text': 'Update Quiz',
    })


@staff_member_required
def delete_quiz(request, quiz_id):
    """Archive a quiz instead of deleting it (soft-delete)"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        title = quiz.title
        quiz.is_active = False
        quiz.save()
        messages.success(request, f'Quiz "{title}" has been moved to the archive.')
        return redirect('quizzes:list')
    
    return render(request, 'pages/confirm_delete.html', {
        'object': quiz,
        'object_type': 'Quiz',
        'cancel_url': reverse('quizzes:detail', kwargs={'quiz_id': quiz_id}),
        'submit_text': 'Move to Archive',
        'warning_text': 'This quiz will no longer be visible to students but can be restored from the archive.'
    })


@staff_member_required
def archived_quizzes_view(request):
    """List all archived quizzes (staff only)"""
    archived_quizzes = Quiz.objects.filter(is_active=False)
    return render(request, 'pages/quiz_archive.html', {
        'quizzes': archived_quizzes,
        'title': 'Quiz Archive (Recycle Bin)'
    })


@staff_member_required
def restore_quiz(request, quiz_id):
    """Restore an archived quiz (staff only)"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=False)
    quiz.is_active = True
    quiz.save()
    messages.success(request, f'Quiz "{quiz.title}" has been restored successfully!')
    return redirect('quizzes:archive')


@staff_member_required
def permanent_delete_quiz(request, quiz_id):
    """Permanently delete a quiz from the archive (staff only)"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=False)
    
    if request.method == 'POST':
        title = quiz.title
        quiz.delete()
        messages.success(request, f'Quiz "{title}" has been permanently deleted.')
        return redirect('quizzes:archive')
    
    return render(request, 'pages/confirm_delete.html', {
        'object': quiz,
        'object_type': 'Quiz',
        'cancel_url': reverse('quizzes:archive'),
        'submit_text': 'Permanently Delete',
        'warning_text': 'CRITICAL: This action cannot be undone. All questions and results linked to this quiz will be lost forever.'
    })


@staff_member_required
def create_question(request, quiz_id):
    """Create a new question for a quiz (staff only)"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = AnswerFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save()
            formset.instance = question
            formset.save()
            messages.success(request, f'Question and answers created successfully!')
            return redirect('quizzes:edit_quiz', quiz_id=quiz.id)
    else:
        form = QuestionForm(initial={'quiz': quiz.id})
        formset = AnswerFormSet()
    
    return render(request, 'pages/question_form.html', {
        'form': form,
        'formset': formset,
        'quiz': quiz,
        'title': f'Add Question to: {quiz.title}',
        'submit_text': 'Create Question',
    })


@staff_member_required
def edit_question(request, question_id):
    """Edit an existing question (staff only)"""
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Question and answers updated successfully!')
            return redirect('quizzes:edit_quiz', quiz_id=quiz.id)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    
    return render(request, 'pages/question_form.html', {
        'form': form,
        'formset': formset,
        'question': question,
        'quiz': quiz,
        'title': f'Edit Question',
        'submit_text': 'Update Question',
    })


@staff_member_required
def delete_question(request, question_id):
    """Delete a question (staff only)"""
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, f'Question deleted successfully!')
        return redirect('quizzes:edit_quiz', quiz_id=quiz_id)
    
    return render(request, 'pages/confirm_delete.html', {
        'object': question,
        'object_type': 'Question',
        'cancel_url': reverse('quizzes:edit_quiz', kwargs={'quiz_id': quiz_id}),
    })


@staff_member_required
def create_answer(request, question_id):
    """Create a new answer for a question (staff only)"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            messages.success(request, f'Answer created successfully!')
            return redirect('quizzes:edit_question', question_id=question.id)
    else:
        form = AnswerForm(initial={'question': question.id})
    
    return render(request, 'pages/answer_form.html', {
        'form': form,
        'question': question,
        'title': f'Add Answer',
        'submit_text': 'Create Answer',
    })


@staff_member_required
def edit_answer(request, answer_id):
    """Edit an existing answer (staff only)"""
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Answer updated successfully!')
            return redirect('quizzes:edit_question', question_id=question.id)
    else:
        form = AnswerForm(instance=answer)
    
    return render(request, 'pages/answer_form.html', {
        'form': form,
        'answer': answer,
        'question': question,
        'title': f'Edit Answer',
        'submit_text': 'Update Answer',
    })


@staff_member_required
def delete_answer(request, answer_id):
    """Delete an answer (staff only)"""
    answer = get_object_or_404(Answer, id=answer_id)
    question_id = answer.question.id
    
    if request.method == 'POST':
        answer.delete()
        messages.success(request, f'Answer deleted successfully!')
        return redirect('quizzes:edit_question', question_id=question_id)
    
    return render(request, 'pages/confirm_delete.html', {
        'object': answer,
        'object_type': 'Answer',
        'cancel_url': 'quizzes:edit_question',
        'cancel_kwargs': {'question_id': question_id},
    })
