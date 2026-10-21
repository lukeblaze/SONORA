import joblib
import numpy as np

# Load the saved model
model = joblib.load("emotion_detection/emotion_model.pkl")

# Example: A random normalized feature vector (flattened image)
example_features = np.random.rand(2304).reshape(1, -1)  # Random test data

# Predict emotion
predicted_emotion = model.predict(example_features)
print(f"Predicted Emotion: {predicted_emotion[0]}")
