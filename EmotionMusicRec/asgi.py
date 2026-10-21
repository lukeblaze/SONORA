import os
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmotionMusicRec.settings')
application = get_asgi_application()
application = get_wsgi_application()
