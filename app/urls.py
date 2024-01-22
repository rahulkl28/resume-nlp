from django.urls import path
from .views import match_skills

urlpatterns = [
    path('match_skills/', match_skills, name='match_skills'),
]