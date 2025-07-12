# models.py
from django.db import models
from django.contrib.auth.models import User

class SkillProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    skills_offered = models.JSONField(default=list)
    skills_wanted = models.JSONField(default=list)
    availability = models.CharField(
        max_length=50,
        choices=[
            ('Weekends', 'Weekends'),
            ('Evenings', 'Evenings'),
            ('Mornings', 'Mornings')
        ]
    )
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SkillSwapRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests', null=True, blank=True)
    skill_offered = models.CharField(max_length=100)
    skill_requested = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    allow_general = models.BooleanField(default=True)

    def __str__(self):
        if self.receiver:
            return f"{self.sender.username} → {self.receiver.username}"
        return f"{self.sender.username} → (anyone)"
