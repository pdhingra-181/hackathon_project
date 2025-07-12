from django.db import models

class SkillProfile(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    availability = models.CharField(max_length=50, choices=[
        ('Weekends', 'Weekends'),
        ('Evenings', 'Evenings'),
        ('Mornings', 'Mornings')
    ])
    skills_offered = models.TextField(help_text="Comma-separated list")
    skills_wanted = models.TextField(help_text="Comma-separated list")
    rating = models.FloatField(default=0.0)

    def get_skills_offered_list(self):
        return [skill.strip() for skill in self.skills_offered.split(',') if skill.strip()]

    def get_skills_wanted_list(self):
        return [skill.strip() for skill in self.skills_wanted.split(',') if skill.strip()]

from django.db import models
from django.contrib.auth.models import User

class SkillProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Changed here
    name = models.CharField(max_length=100)
    skills_offered = models.JSONField(default=list)
    skills_wanted = models.JSONField(default=list)
    availability = models.CharField(max_length=50)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SkillSwapRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    skill_offered = models.CharField(max_length=100)
    skill_requested = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"
