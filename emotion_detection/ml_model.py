import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
# Print working directory and dataset path
print("Current working directory:", os.getcwd())

# Specify dataset path
data_path = r"C:\Users\PC\Desktop\School\Sep-Dec 2024 semester\Cloud Computing Project\app\emotion_detection\datasets\fer2013.csv"
print(f"Dataset path being used: {data_path}")

def load_data(data_path):
    """Loads data from a CSV file."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    print(f"Loading dataset from: {data_path}")
    data = pd.read_csv(data_path)
    return data

def preprocess_data(data, numerical_feature):
    """Preprocesses the data."""
    # Fill missing values
    data = data.ffill()


    # Scale numerical features
    scaler = StandardScaler()
    data[numerical_feature] = data[numerical_feature].apply(
        lambda x: np.fromstring(x, sep=" ").reshape(-1) / 255.0
    )
    data = data[numerical_feature].apply(pd.Series)  # Expand into columns

    return data

def split_data(data, target_column):
    """Splits the data into training and testing sets."""
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Trains a logistic regression model."""
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluates the model's performance."""
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def save_model(model, file_path):
    """Saves the trained model to a file."""
    joblib.dump(model, file_path)
    print(f"Model saved to {file_path}")

if __name__ == "__main__":
    # Load the data
    data = load_data(data_path)

    # Define features and target column
    target_column = 'emotion'  # FER2013 target column
    numerical_feature = 'pixels'  # FER2013 pixel column

    # Preprocess the data
    preprocessed_data = preprocess_data(data, numerical_feature)
    preprocessed_data[target_column] = data[target_column]  # Add the target column back

    # Split data
    X_train, X_test, y_train, y_test = split_data(preprocessed_data, target_column)

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

    # Save the model
    save_model(model, "emotion_model.pkl")
