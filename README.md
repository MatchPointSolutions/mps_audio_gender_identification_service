# MPS AUDIO ANALYSER

## Overview:

`MPS AUDIO ANALYSER`  identifies the number of Male voices, Female voices, Child voices, and Background music in an audio file which uses Machine Learning Models for identifying the Male and Female voices, later for identifying the music in an audio file it uses Acoust id service.

Demo URI: https://audioanalyzer.matchps.com/

## Table of Contents

- Prerequisites
- Installation
- Usage
- Dependencies
- Machine Learning Models
- AcoustID Integration
- Environment Variables

## Prerequisites:
-   [python >=3.9](https://www.python.org/downloads/)
-   [gradio==4.9.1](https://pypi.org/project/gradio/4.9.1/)

## Installation:
clone the repository ```https://github.com/matchps/mps_audio_gender_identification_service.git```

Install the required dependencies ```pip install -r requirements.txt```

## Usage:
fastapi service - ``` py mps_audio_fast_api/main.py ```

gradio service - ``` py mps_audio_gradio/main.py ```

Access the Gradio UI by visiting http://localhost:8000 in your web browser.

Upload an audio file through the Gradio interface to trigger the analysis.

## Dependencies
- FastAPI
- Gradio
- Python
- AcoustID
- Scikit-learn

## Machine Learning Models

The Audio Analyzer uses two machine learning models for voice classification:

```Random Forest Model```
: A machine learning model based on the Random Forest algorithm. This model is trained to recognize different voice characteristics.

```Support Vector Machine (SVM)```
: A machine learning model based on the Support Vector Machine algorithm. It is designed to classify voice characteristics in the given audio file.

For Male and Female voice classification we have reached accuracy score of 80% and for Child voice classification we have reached 60% of accuracy score.

## AcoustID Integration
The Audio Analyzer integrates with the AcoustID database to identify background music in the uploaded audio files. AcoustID provides a fingerprinting service that matches audio fingerprints to their corresponding metadata in the database.

## Environment Variables


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `LOG_FILE_PATH` | `filepath` | **Required**. Set log file name for storing the logs |
| `MODEL_FILENAME` | `filepath` | **Required**. set trained model file path |
| `ACCESS_TOKEN` | `string` | **Required**. hugging face access token for pyannote |
| `ACOUST_ID_TOKEN` | `string` | **Required**. Your Acoust id token |
| `SMTP_SERVER` | `string` | **Required**. Auto Email notification setup |
| `SMTP_PORT` | `int` | **Required**. Auto Email notification setup |
| `SMTP_USER` | `string` | **Required**. Auto Email notification setup |
| `SMTP_PASSWORD` | `string` | **Required**. Auto Email notification setup |
| `SUBJECT` | `string` | **Required**. Subject to send in email |
| `DATASET` | `xlsx` | trained model datset |
| `FASTAPI_URL` | `url` | |
