"""
    This Code Trains the Model to identify the Male and Female voice in the given audio.
    It was trained on 196000 recorded audio files.
"""
import os
import librosa
import joblib
import numpy as np
import pandas as pd
from config import DATASET,MODEL_FILENAME
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from log import setup_logger
logger = setup_logger(__name__)


def extract_features_1(file_path, max_len=100):
    """
        Extract Features from the audio file
    """
    audio, _ = librosa.load(file_path, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=librosa.get_samplerate(file_path), n_mfcc=13)
    if mfccs.shape[1] < max_len:
        pad_width = max_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfccs = mfccs[:, :max_len]

    return mfccs.flatten()


def train_model(df):
    """
        This code trains the Model and Recognize the gives audio input
    """
    dataset_path = DATASET
    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=['gender'])
    logger.info(len(df))
    df['features'] = df['filename'].apply(lambda x: extract_features_1(os.path.join("C://Users/ChintalapudiTejaswin/Downloads/audiodataset/cv-valid-train", x)))
    logger.info(df.head(10))
    df['gender_encoded'] = df['gender'].map({'male': 0, 'female': 1})
    mean_value = df['gender_encoded'].median()
    df['gender_encoded'].fillna(mean_value, inplace=True)
    logger.info(df.head(10))
    X_train, X_test, y_train, y_test = train_test_split(df['features'].tolist(), df['gender_encoded'].tolist(), test_size=0.2, random_state=42)
    logger.info("-------------Training the Model---------------------")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logger.info("---------------------------Predicting the Model----------------------")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy}")
    logger.info("Classification Report:")
    logger.info(report)
    joblib.dump(model, MODEL_FILENAME)
    logger.info(f"Model saved to {MODEL_FILENAME}")

# Train the Model
# train_model(df)

def identify_the_audio(input_file,model_filename=MODEL_FILENAME):
    """
        Identifies the input audio file
    """
    loaded_model = joblib.load(model_filename)
    new_audio_features = extract_features_1(input_file)
    prediction = loaded_model.predict([new_audio_features])
    logger.info(f"Predicted gender: {'female' if prediction[0] == 1 else 'male'}")
    if prediction[0] == 1:
        return "female"
    else:
        return "male"



