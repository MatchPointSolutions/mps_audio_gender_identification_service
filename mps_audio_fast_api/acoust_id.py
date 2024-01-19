"""
The code accepts the acoust_id token to access the acoust id database to search
the audio file background music
"""
import requests
import subprocess
from config import ACOUST_ID_TOKEN
from log import setup_logger
logger = setup_logger(__name__)


def calculate_fingerprints(filename):
    """
    Args: filename (audio file path)
    -   here the fpcalc is used to convert audio file to fingerprint and calculate total duration.
        If there are any errors in converting or calculating, it will return None for both values.
    Output: fingerprint, duration
    """
    duration = ""
    fingerprint = ""
    command = ['fpcalc', filename]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:
                data = str(result.stdout)
                logger.info(data)
                duration_index = data.find('DURATION=') + len('DURATION=')
                duration_end_index = data.find('\n', duration_index)
                duration = int(data[duration_index:duration_end_index])
                fingerprint_index = data.find('FINGERPRINT=') + len('FINGERPRINT=')
                fingerprint = data[fingerprint_index:].strip()
                # logger.info(fingerprint)
                logger.info("Duration: {}".format(duration))
                return duration, fingerprint
        elif result.stderr:
                data = str(result.stderr)
                logger.info(data)
                duration_index = data.find('DURATION=') + len('DURATION=')
                duration_end_index = data.find('\n', duration_index)
                duration = int(data[duration_index:duration_end_index])
                fingerprint_index = data.find('FINGERPRINT=') + len('FINGERPRINT=')
                fingerprint = data[fingerprint_index:].strip()
                # logger.info(fingerprint)
                logger.info("Duration: {}".format(duration))
                return duration, fingerprint
        else:
            logger.info("No output from fpcalc")
            logger.info("Duration: {}".format(duration))
            logger.info("Fingerprint: {}".format(fingerprint))
            return duration, fingerprint
    except Exception as error:
         logger.info(f"in calculate_fingerprints: couldn't calculate fingerprint for the given file: {error}")
         return duration, fingerprint


def get_acoust_id_audio_details(file_path):
    """
    Args: file_path (audio file path)
    -   This function uses AcoustId API to fetch details of an audio file like genre, artist etc.
        if the database doesn't contain details it returns empty results
    Output: dict with keys 'genre','artist','title' and their corresponding values
    """
    try:
        duration,fingerprint = calculate_fingerprints(file_path)
    except Exception as error:
        duration = ""
        fingerprint = ""
        logger.info(f"in get_acoust_id_audio_details: couldn't calculate fingerprint for the given file: {error}")

    if fingerprint != "":
        api_key = ACOUST_ID_TOKEN
        try:
            url = f"""https://api.acoustid.org/v2/lookup?client={api_key}&meta=recordings+releasegroups+compress&duration={duration}&fingerprint={fingerprint}"""
            logger.info(url)
            response = requests.get(url)
            data = response.json()
            logger.info(f"data extracted!!!!")
            return data
        except Exception as error:
            logger.info(f"in get_acoust_id_audio_details: couldn't find the relavant details for the audio: {error}")
            return { "results": [] }
    else:
         logger.info(f"in get_acoust_id_audio_details: couldn't generate fingerprint for the given file: {error}")
         return {"results": []}
