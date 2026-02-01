from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from .models import Course, Lesson, UserCourseProgress
from .forms import CourseForm, LessonForm


@login_required
def course_list_view(request):
    """Display all published courses (excluding archived)"""
    courses = Course.objects.filter(is_published=True, is_archived=False)
    return render(request, 'pages/course_list.html', {'courses': courses})


@login_required
def course_detail_view(request, course_id):
    """Display course details and lessons"""
    # Staff can view archived courses, regular users cannot
    if request.user.is_staff:
        course = get_object_or_404(Course, id=course_id)
    else:
        course = get_object_or_404(Course, id=course_id, is_published=True, is_archived=False)
    lessons = course.lessons.all()
    
    # Get or create user progress if authenticated
    progress = None
    if request.user.is_authenticated:
        progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course
        )
    
    context = {
        'course': course,
        'lessons': lessons,
        'progress': progress,
    }
    return render(request, 'pages/course_detail.html', context)


@login_required
def lesson_view(request, course_id, lesson_id):
    """Display lesson content"""
    course = get_object_or_404(Course, id=course_id, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Get or create progress
    progress, created = UserCourseProgress.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    # Get previous and next lessons
    all_lessons = list(course.lessons.all())
    current_index = all_lessons.index(lesson)
    previous_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    
    # Check if lesson is completed
    is_completed = progress.completed_lessons.filter(id=lesson_id).exists()
    
    context = {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'is_completed': is_completed,
    }
    return render(request, 'pages/lesson.html', context)


@login_required
def mark_lesson_complete(request, course_id, lesson_id):
    """Mark a lesson as complete"""
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    progress, created = UserCourseProgress.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    # Add lesson to completed lessons
    if not progress.completed_lessons.filter(id=lesson_id).exists():
        progress.completed_lessons.add(lesson)
        messages.success(request, f'Lesson "{lesson.title}" marked as complete!')
    
    # Check if all lessons are completed
    if progress.progress_percentage == 100 and not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, f'Congratulations! You completed the course "{course.title}"!')
    
    # Redirect to next lesson or back to course
    all_lessons = list(course.lessons.all())
    current_index = all_lessons.index(lesson)
    if current_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_index + 1]
        return redirect('courses:lesson', course_id=course_id, lesson_id=next_lesson.id)
    else:
        return redirect('courses:detail', course_id=course_id)


# Content Management Views

@staff_member_required
def create_course(request):
    """Create a new course (staff only)"""
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('courses:detail', course_id=course.id)
    else:
        form = CourseForm()
    
    return render(request, 'pages/course_form.html', {
        'form': form,
        'title': 'Create New Course',
        'submit_text': 'Create Course',
    })


@staff_member_required
def edit_course(request, course_id):
    """Edit an existing course (staff only)"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.title}" updated successfully!')
            return redirect('courses:detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'pages/course_form.html', {
        'form': form,
        'course': course,
        'title': f'Edit Course: {course.title}',
        'submit_text': 'Update Course',
    })


@staff_member_required
def delete_course(request, course_id):
    """Delete a course (staff only)"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'Course "{title}" deleted successfully!')
        return redirect('courses:list')
    
    return render(request, 'pages/confirm_delete.html', {
        'object': course,
        'object_type': 'Course',
        'cancel_url': reverse('courses:detail', kwargs={'course_id': course_id}),
    })


@staff_member_required
def create_lesson(request, course_id=None):
    """Create a new lesson (staff only)"""
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, f'Lesson "{lesson.title}" created successfully!')
            return redirect('courses:detail', course_id=lesson.course.id)
    else:
        # Pre-select course if provided
        initial = {}
        if course_id:
            initial['course'] = course_id
        form = LessonForm(initial=initial)
    
    return render(request, 'pages/lesson_form.html', {
        'form': form,
        'title': 'Create New Lesson',
        'submit_text': 'Create Lesson',
    })


@staff_member_required
def edit_lesson(request, lesson_id):
    """Edit an existing lesson (staff only)"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lesson "{lesson.title}" updated successfully!')
            return redirect('courses:detail', course_id=lesson.course.id)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'pages/lesson_form.html', {
        'form': form,
        'lesson': lesson,
        'title': f'Edit Lesson: {lesson.title}',
        'submit_text': 'Update Lesson',
    })


@staff_member_required
def delete_lesson(request, lesson_id):
    """Delete a lesson (staff only)"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course.id
    
    if request.method == 'POST':
        title = lesson.title
        lesson.delete()
        messages.success(request, f'Lesson "{title}" deleted successfully!')
        return redirect('courses:detail', course_id=course_id)
    
    return render(request, 'pages/confirm_delete.html', {
        'object': lesson,
        'object_type': 'Lesson',
        'cancel_url': reverse('courses:detail', kwargs={'course_id': course_id}),
    })


# Archive Management Views

@staff_member_required
def archive_course(request, course_id):
    """Archive a course (soft delete)"""
    course = get_object_or_404(Course, id=course_id)
    course.is_archived = True
    course.save()
    messages.success(request, f'Course "{course.title}" has been archived.')
    return redirect('courses:list')


@staff_member_required
def restore_course(request, course_id):
    """Restore an archived course"""
    course = get_object_or_404(Course, id=course_id, is_archived=True)
    course.is_archived = False
    course.save()
    messages.success(request, f'Course "{course.title}" has been restored.')
    return redirect('courses:archived')


@staff_member_required
def archived_courses_view(request):
    """Display all archived courses (staff only)"""
    courses = Course.objects.filter(is_archived=True)
    return render(request, 'pages/archived_courses.html', {'courses': courses})


@staff_member_required
def video_diagnostic_view(request):
    """Diagnostic page to view all video URLs and their conversions (staff only)"""
    lessons = Lesson.objects.filter(video_url__isnull=False).exclude(video_url='')
    return render(request, 'pages/video_diagnostic.html', {'lessons': lessons})

