from django.contrib import admin
from .models import Quiz, Question, Answer, UserQuizAttempt


class AnswerInline(admin.TabularInline):
    """Inline admin for answers within question"""
    model = Answer
    extra = 4
    fields = ('text', 'is_correct')


class QuestionInline(admin.StackedInline):
    """Inline admin for questions within quiz"""
    model = Question
    extra = 1
    fields = ('text', 'order')
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin interface for Quiz"""
    list_display = ('title', 'course', 'question_count', 'passing_score', 'time_limit_minutes', 'is_active', 'created_at')
    list_filter = ('is_active', 'course', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Quiz Information', {
            'fields': ('title', 'description', 'course', 'is_active')
        }),
        ('Settings', {
            'fields': ('passing_score', 'time_limit_minutes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question"""
    list_display = ('quiz', 'text_preview', 'order', 'created_at')
    list_filter = ('quiz', 'created_at')
    search_fields = ('text', 'quiz__title')
    inlines = [AnswerInline]
    ordering = ('quiz', 'order')
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin interface for Answer"""
    list_display = ('question_preview', 'text_preview', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('text', 'question__text')
    
    def question_preview(self, obj):
        return obj.question.text[:30] + '...'
    question_preview.short_description = 'Question'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Answer Text'


@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface for UserQuizAttempt"""
    list_display = ('user', 'quiz', 'score', 'passed', 'time_taken_minutes', 'attempted_at')
    list_filter = ('attempted_at', 'quiz')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('attempted_at', 'passed', 'correct_count', 'incorrect_count')
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('user', 'quiz', 'score', 'time_taken_minutes')
        }),
        ('Results', {
            'fields': ('passed', 'correct_count', 'incorrect_count')
        }),
        ('Details', {
            'fields': ('answers', 'attempted_at'),
            'classes': ('collapse',)
        }),
    )
