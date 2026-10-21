import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

EMOTION_LABELS = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Neutral']
_model = None


def home(request):
    return render(request, 'emotion_detection/home.html')


def _load_model():
    global _model
    if _model is None:
        try:
            from keras.models import load_model
            model_path = os.path.join(settings.BASE_DIR, 'emotion_detection', 'emotion_model.h5')
            _model = load_model(model_path, compile=False)
        except (ImportError, OSError, ValueError):
            _model = False
    return _model


def _predict_emotion(image):
    model = _load_model()
    if model:
        try:
            import numpy as np
            grayscale = image.convert('L').resize((48, 48))
            pixels = np.asarray(grayscale, dtype='float32') / 255.0
            predictions = model.predict(pixels.reshape(1, 48, 48, 1), verbose=0)
            index = int(np.argmax(predictions[0]))
            return EMOTION_LABELS[index], round(float(np.max(predictions[0])) * 100, 1), 'model'
        except (IndexError, TypeError, ValueError):
            pass
    return 'Happiness', 78.0, 'demo'


@csrf_exempt
def detect_emotion(request):
    if request.method != 'POST' or not request.FILES.get('file'):
        return JsonResponse({'error': 'Choose an image before detecting your emotion.'}, status=400)
    try:
        image = Image.open(request.FILES['file'])
        emotion, confidence, source = _predict_emotion(image)
        return JsonResponse({
            'emotion': emotion,
            'confidence': confidence,
            'source': source,
            'songs': get_song_recommendations(emotion),
        })
    except (OSError, ValueError):
        return JsonResponse({'error': 'That file could not be read as an image.'}, status=400)


@csrf_exempt
def detect_emotion_from_file(request):
    return detect_emotion(request)


@csrf_exempt
def detect_emotion_from_camera(request):
    return detect_emotion(request)


def get_song_recommendations(emotion):
    playlists = {
        'happiness': [
            ('Good as Hell', 'Lizzo', 'upbeat pop'),
            ('Lovely Day', 'Bill Withers', 'soul classic'),
            ('Walking on Sunshine', 'Katrina & The Waves', 'feel-good'),
        ],
        'sadness': [
            ('Fix You', 'Coldplay', 'reflective'),
            ('A Sky Full of Stars', 'Coldplay', 'hopeful'),
            ('Keep Your Head Up', 'Ben Howard', 'acoustic'),
        ],
        'anger': [
            ('Dog Days Are Over', 'Florence + The Machine', 'release'),
            ('Titanium', 'David Guetta ft. Sia', 'powerful'),
            ('The Pretender', 'Foo Fighters', 'rock energy'),
        ],
        'fear': [
            ('Brave', 'Sara Bareilles', 'uplifting'),
            ('Three Little Birds', 'Bob Marley & The Wailers', 'calm'),
            ('Here Comes the Sun', 'The Beatles', 'warm'),
        ],
        'neutral': [
            ('Put Your Records On', 'Corinne Bailey Rae', 'easy listening'),
            ('Sunset Lover', 'Petit Biscuit', 'electronic'),
            ('Dreams', 'Fleetwood Mac', 'classic'),
        ],
        'surprise': [
            ('Electric Feel', 'MGMT', 'bright'),
            ('Levitating', 'Dua Lipa', 'dance pop'),
            ('Everybody Wants to Rule the World', 'Tears for Fears', 'classic'),
        ],
        'disgust': [
            ('Shake It Out', 'Florence + The Machine', 'reset'),
            ('Three Little Birds', 'Bob Marley & The Wailers', 'calm'),
            ('Lovely Day', 'Bill Withers', 'soul classic'),
        ],
    }
    tracks = playlists.get(emotion.lower(), playlists['neutral'])
    return [
        {'id': index + 1, 'song_name': name, 'artist': artist, 'mood': mood,
         'link': 'https://open.spotify.com/search/' + name.replace(' ', '%20')}
        for index, (name, artist, mood) in enumerate(tracks)
    ]
