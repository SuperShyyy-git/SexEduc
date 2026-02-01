from django.contrib import admin
from .models import Course, Lesson, UserCourseProgress


class LessonInline(admin.TabularInline):
    """Inline admin for lessons within course"""
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'duration_minutes', 'video_url')
    ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course"""
    list_display = ('title', 'difficulty', 'lesson_count', 'enrolled_count', 'is_published', 'created_at')
    list_filter = ('difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'image', 'difficulty', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for Lesson"""
    list_display = ('title', 'course', 'order', 'duration_minutes', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content', 'course__title')
    ordering = ('course', 'order')
    
    fieldsets = (
        ('Lesson Information', {
            'fields': ('course', 'title', 'content', 'video_url', 'order', 'duration_minutes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    """Admin interface for UserCourseProgress"""
    list_display = ('user', 'course', 'progress_percentage', 'completed', 'started_at')
    list_filter = ('completed', 'started_at', 'course')
    search_fields = ('user__username', 'course__title')
    filter_horizontal = ('completed_lessons',)
    readonly_fields = ('started_at', 'progress_percentage')
    
    fieldsets = (
        ('Progress Information', {
            'fields': ('user', 'course', 'completed', 'completed_at')
        }),
        ('Lessons', {
            'fields': ('completed_lessons',)
        }),
        ('Timestamps', {
            'fields': ('started_at',),
            'classes': ('collapse',)
        }),
    )
