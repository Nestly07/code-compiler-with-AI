from django.db import models

class User(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.username

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

DIFFICULTY_CHOICES = [
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]

# If not found in settings, fallback
DIFFICULTY_POINTS= getattr(settings, 'DIFFICULTY_POINTS', {
    'easy': 10,
    'medium': 20,
    'hard': 30,
})
class CodingChallenge(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')

    description = models.TextField(help_text="Problem statement / description (Markdown allowed)")
    input_format = models.TextField(blank=True, default="")
    output_format = models.TextField(blank=True, default="")
    constraints = models.TextField(blank=True, default="")

    sample_input = models.TextField(blank=True, default="")
    sample_output = models.TextField(blank=True, default="")

    test_input = models.TextField(blank=True, default="", help_text="Hidden input for judging")
    expected_output = models.TextField(blank=True, default="", help_text="Expected exact output for judging")
    max_runtime_ms = models.PositiveIntegerField(default=2000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['difficulty', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def points(self) -> int:
        return DIFFICULTY_POINTS.get(self.difficulty, 0)

    def get_absolute_url(self):
        return reverse('compiler:challenge_detail', args=[self.slug])
LANGUAGE_CHOICES = [
    ("python", "Python 3"),
    ("c", "C (GCC)"),
    ("cpp", "C++ (G++)"),
    ("java", "Java (OpenJDK)"),
]

STATUS_CHOICES = [
    ("queued", "Queued"),
    ("running", "Running"),
    ("accepted", "Accepted"),
    ("wrong_answer", "Wrong Answer"),
    ("time_limit", "Time Limit Exceeded"),
    ("runtime_error", "Runtime Error"),
    ("compilation_error", "Compilation Error"),
    ("failed", "Failed"),
]

class Submission(models.Model):
    challenge = models.ForeignKey(CodingChallenge, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.SET_NULL, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True, default="",null=True, help_text="Guest name if not logged in")

    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="python")
    source_code = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    result_output = models.TextField(blank=True, default="")
    result_stderr = models.TextField(blank=True, default="")
    time_ms = models.PositiveIntegerField(default=0)
    memory_kb = models.PositiveIntegerField(default=0)

    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        who = self.display_name or (self.user.get_username() if self.user else "Anonymous")
        return f"{who} -> {self.challenge.title} [{self.status}]"


class Leaderboard(models.Model):
    """Materialized leaderboard (optional).
    You can also compute leaderboard on the fly with aggregation.
    """
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True, default="")
    total_points = models.IntegerField(default=0)
    last_submission_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Leaderboard Entry"
        verbose_name_plural = "Leaderboard"
        ordering = ['-total_points', '-last_submission_at']

    def __str__(self):
        name = self.display_name or (self.user.get_username() if self.user else "Anonymous")
        return f"{name} – {self.total_points} pts"


from django.db import models
from django.contrib.auth.models import User
class CodeSubmission(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    language=models.CharField(max_length=50)
    code=models.TextField()
    output=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    message=models.TextField()
    reply=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)