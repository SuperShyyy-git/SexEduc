from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """Course model for educational content"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def lesson_count(self):
        return self.lessons.count()
    
    @property
    def enrolled_count(self):
        return UserCourseProgress.objects.filter(course=self).count()


class Lesson(models.Model):
    """Lesson model for course content"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or other video URL")
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=10, help_text="Estimated time to complete in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class UserCourseProgress(models.Model):
    """Track user progress through courses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress')
    completed_lessons = models.ManyToManyField(Lesson, blank=True, related_name='completed_by_users')
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name_plural = 'User course progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    @property
    def progress_percentage(self):
        """Calculate completion percentage"""
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return 0
        completed = self.completed_lessons.count()
        return round((completed / total_lessons) * 100)
    
    @property
    def passed(self):
        """Check if user has completed all lessons"""
        return self.progress_percentage == 100
