from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class Quiz(models.Model):
    """Quiz model for assessments"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    passing_score = models.PositiveIntegerField(default=70, help_text="Percentage required to pass")
    time_limit_minutes = models.PositiveIntegerField(default=30, help_text="Time limit in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return self.title
    
    @property
    def question_count(self):
        return self.questions.count()
    
    @property
    def total_points(self):
        return self.questions.count()  # Each question worth 1 point


class Question(models.Model):
    """Question model for quiz questions"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.text[:50]}"
    
    @property
    def correct_answer(self):
        return self.answers.filter(is_correct=True).first()


class Answer(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:30]}"


class UserQuizAttempt(models.Model):
    """Track user quiz attempts and scores"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0.0)  # Percentage score
    answers = models.JSONField(default=dict, help_text="Store user's answers as {question_id: answer_id}")
    attempted_at = models.DateTimeField(auto_now_add=True)
    time_taken_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}%"
    
    @property
    def passed(self):
        return self.score >= self.quiz.passing_score
    
    @property
    def correct_count(self):
        """Count of correct answers"""
        return int((self.score / 100) * self.quiz.question_count)
    
    @property
    def incorrect_count(self):
        """Count of incorrect answers"""
        return self.quiz.question_count - self.correct_count
