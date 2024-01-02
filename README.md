# MPS AUDIO ANALYSER

## WorkFlow:

-   The code works on identifying the number of Male voices, Female voices and Background music in an audio file.
-   The Implemented Machine Learning Model was trained on identifying the Male and Female voices.
-   The Acoust id service is used to identify the background music being played in the audio file.

## Prerequisites:
-   ` python >=3.9 `
-   ` gradio==4.9.1 `

## RUN:
fastapi service - ``` py mps_audio_fast_api/main.py ```

gradio service - ``` py mps_audio_gradio/main.py ```

## Environment Variables


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `LOG_FILE_PATH` | `path` | **Required**. Set log file name for storing the logs |
| `MODEL_FILENAME` | `string` | **Required**. set trained model file path |
| `ACCESS_TOKEN` | `string` | **Required**. hugging face access token for pyannote |
| `ACOUST_ID_TOKEN` | `string` | **Required**. Your Acoust id token |
| `SMTP_SERVER` | `string` | **Required**. Auto Email notification setup |
| `SMTP_PORT` | `string` | **Required**. Auto Email notification setup |
| `SMTP_USER` | `string` | **Required**. Auto Email notification setup |
| `SMTP_PASSWORD` | `string` | **Required**. Auto Email notification setup |
| `SUBJECT` | `string` | **Required**. Subject to send in email |
| `DATASET` | `string` | trained model datset |
| `FASTAPI_URL` | `string` | |
