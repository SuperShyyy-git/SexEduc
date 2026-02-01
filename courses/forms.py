from django import forms
from .models import Course, Lesson, UserCourseProgress


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses"""
    
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'difficulty', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter course title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Enter course description',
                'rows': 6,
            }),
            'image': forms.FileInput(attrs={
                'class': 'input-field',
                'accept': 'image/*',
            }),
            'difficulty': forms.Select(attrs={
                'class': 'input-field',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'input-checkbox',
            }),
        }
        labels = {
            'title': 'Course Title',
            'description': 'Course Description',
            'image': 'Course Image',
            'difficulty': 'Difficulty Level',
            'is_published': 'Publish this course',
        }


class LessonForm(forms.ModelForm):
    """Form for creating and editing lessons"""
    
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'video_url', 'order']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'input-field',
            }),
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter lesson title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Enter lesson content',
                'rows': 10,
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'input-field',
                'placeholder': 'https://youtube.com/watch?v=...',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'input-field',
                'min': 1,
            }),
        }
        labels = {
            'course': 'Select Course',
            'title': 'Lesson Title',
            'content': 'Lesson Content',
            'video_url': 'Video URL (Optional)',
            'order': 'Lesson Order',
        }
