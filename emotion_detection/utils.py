import joblib
import numpy as np
from django.urls import path

from emotion_detection import views

model = joblib.load("emotion_detection/emotion_model.pkl")
path('emotion/detect-from-camera/', views.detect_emotion_from_file, name='detect_emotion_from_camera'),


def predict_emotion(features):
    features = np.array(features).reshape(1, -1)
    emotion = model.predict(features)
    return emotion[0]
def detect_emotion_from_features(features):
    """
    Dummy function to detect emotion from features.
    Replace this with actual emotion detection logic.
    """
    # Example logic for demonstration
    if "happy" in features:
        return "Happy"
    elif "sad" in features:
        return "Sad"
    else:
        return "Neutral"