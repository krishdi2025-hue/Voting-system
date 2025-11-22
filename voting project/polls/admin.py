from django.contrib import admin
from .models import Candidate, Vote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('number','name')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('candidate','created_at','session_key','user')
