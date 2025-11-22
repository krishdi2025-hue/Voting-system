from django.db import models
from django.conf import settings

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=0)
    photo = models.CharField(max_length=500, blank=True)
    symbol = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.number}. {self.name}"

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote for {self.candidate} at {self.created_at}"
