import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore
from sklearn.model_selection import train_test_split

# Path to your dataset
dataset_path = 'C:/Users/PC/Desktop/School/Sep-Dec 2024 semester/Cloud Computing Project/app/emotion_detection/datasets/fer2013.csv'

def load_and_preprocess_data():
    # Load the dataset
    data = pd.read_csv(dataset_path)
    
    # Extract features and labels
    pixels = data['pixels'].values
    emotions = data['emotion'].values

    # Convert pixel strings to numpy arrays
    X = np.array([np.fromstring(pixel, sep=' ').reshape(48, 48, 1) for pixel in pixels])
    X = X / 255.0  # Normalize pixel values

    # One-hot encode labels
    y = to_categorical(emotions, num_classes=7)

    return X, y

def build_model():
    # Define the CNN model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        MaxPooling2D((2, 2)),
        Dropout(0.2),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.3),
        
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(7, activation='softmax')  # 7 classes for emotions
    ])
    
    # Compile the model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    # Load and preprocess data
    print("Loading and preprocessing data...")
    X, y = load_and_preprocess_data()

    # Split into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build the model
    print("Building the model...")
    model = build_model()

    # Train the model
    print("Training the model...")
    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_val, y_val))

    # Save the model
    model.save('emotion_model.h5')
    print("Model saved as 'emotion_model.h5'")

if __name__ == "__main__":
    main()
