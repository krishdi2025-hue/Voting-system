from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('vote/', views.cast_vote, name='cast_vote'),
    path('status/', views.voting_status, name='voting_status'),
]
