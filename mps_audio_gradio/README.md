# MPS AUDIO ANALYSER

## WorkFlow:
-   The Gradio service is used as UI interface for uploading audio file for analysis
-   The code works on identifying the number of Male voices, Female voices and Background music in an audio file.
-   The Implemented Machine Learning Model was trained on identifying the Male and Female voices.
-   The Acoust id service is used to identify the background music being played in the audio file.

## Prerequisites:
-   ` python >=3.9 `
-   ` gradio==4.9.1 `

## RUN:

gradio service - ``` py mps_audio_gradio/main.py ```

## Environment Variables


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `LOG_FILE_PATH` | `path` | **Required**. Set log file name for storing the logs |
| `FASTAPI_URL` | `string` | |


