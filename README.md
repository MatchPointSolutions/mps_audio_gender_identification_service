# MPS AUDIO ANALYSER

## Summary:

`MPS AUDIO ANALYSER`  identifys the number of Male voices, Female voices, Child voices and Background music in an audio file which uses Machine Learning Models for identifying the Male and Female voices, later for identifying the music in an audio file it uses Acoust id service.

## Prerequisites:
-   [python >=3.9](https://www.python.org/downloads/)
-   [gradio==4.9.1](https://pypi.org/project/gradio/4.9.1/)

## RUN:
fastapi service - ``` py mps_audio_fast_api/main.py ```

gradio service - ``` py mps_audio_gradio/main.py ```

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
