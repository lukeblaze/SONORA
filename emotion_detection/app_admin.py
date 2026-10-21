from django.contrib import admin
from .models import Emotion, SongRecommendation

admin.site.register(Emotion)
admin.site.register(SongRecommendation)
