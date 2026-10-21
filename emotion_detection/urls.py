from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'emotion_detection'  # This defines the namespace


urlpatterns = [
    path('', views.home, name='home'),
    path('emotion/detect-from-file/', views.detect_emotion_from_file, name='detect_emotion_from_file'),
    path('emotion/detect-from-camera/', views.detect_emotion_from_camera, name='detect_emotion_from_camera'),
    path('detect-emotion/', views.detect_emotion, name='detect_emotion'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)