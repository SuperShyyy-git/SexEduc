from django import forms
from .models import Quiz, Question, Answer


class QuizForm(forms.ModelForm):
    """Form for creating and editing quizzes"""
    
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'course', 'passing_score', 'time_limit_minutes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter quiz title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Enter quiz description',
                'rows': 4,
            }),
            'course': forms.Select(attrs={
                'class': 'input-field',
            }),
            'passing_score': forms.NumberInput(attrs={
                'class': 'input-field',
                'min': 0,
                'max': 100,
                'value': 70,
            }),
            'time_limit_minutes': forms.NumberInput(attrs={
                'class': 'input-field',
                'min': 1,
                'placeholder': 'Time limit in minutes',
            }),
        }
        labels = {
            'title': 'Quiz Title',
            'description': 'Quiz Description',
            'course': 'Select Course',
            'passing_score': 'Pass Percentage (%)',
            'time_limit_minutes': 'Time Limit (minutes)',
        }


class QuestionForm(forms.ModelForm):
    """Form for creating and editing questions"""
    
    class Meta:
        model = Question
        fields = ['quiz', 'text', 'order']
        widgets = {
            'quiz': forms.HiddenInput(),
            'text': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Enter your question',
                'rows': 3,
            }),
            'order': forms.NumberInput(attrs={
                'class': 'input-field',
                'min': 1,
            }),
        }
        labels = {
            'quiz': 'Select Quiz',
            'text': 'Question Text',
            'order': 'Question Order',
        }


from django.forms import inlineformset_factory

class AnswerForm(forms.ModelForm):
    """Form for creating and editing answers"""
    
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter answer text',
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'input-checkbox',
            }),
        }
        labels = {
            'text': 'Answer Text',
            'is_correct': 'Correct Answer',
        }

# Inline formset for managing answers within the question form
AnswerFormSet = inlineformset_factory(
    Question, 
    Answer, 
    form=AnswerForm,
    extra=4,        # 4 empty answer slots by default
    can_delete=True # Allow deleting existing answers
)
