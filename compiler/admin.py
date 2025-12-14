from django.contrib import admin
from .models import CodingChallenge, Submission, Leaderboard

# Correct way to register
from django.contrib import admin
from .models import CodingChallenge, Submission, Leaderboard

@admin.register(CodingChallenge)
class CodingChallengeAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "points", "created_at")
    list_filter = ("difficulty",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("challenge", "language", "status", "score", "created_at")
    list_filter = ("status", "language")
    search_fields = ("challenge__title", "display_name", "result_output", "result_stderr")

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "total_points", "last_submission_at")
    search_fields = ("display_name", "user__username")


