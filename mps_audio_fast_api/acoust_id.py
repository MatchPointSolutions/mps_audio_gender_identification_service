import requests
import subprocess
from config import ACOUST_ID_TOKEN
from log import setup_logger
logger = setup_logger(__name__)




def generate_fingerprint(file_path):
    try:
        result = subprocess.run(
            ['ffmpeg', '-i', file_path, '-f', 'chromaprint', '-'],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stderr
        logger.info(output)
        return output
    except subprocess.CalledProcessError as error:
        logger.error(f"Error generating fingerprint: {error}")
        logger.info(f"Error generating fingerprint: {error}")
        return {"message": "Error generating fingerprint"}


def calculate_fingerprints(filename):
    command = ['fpcalc', filename]
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


def get_duration(file_path):
    try:
        result = subprocess.run(['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
                                capture_output=True, text=True)
        duration = float(result.stdout.strip())
        logger.info(f"duration: {duration}")
        return duration
    except Exception as error:
        logger.info(f"Error getting audio duration: {error}")
        return {"message":"Unable to get audio duration" }


def get_acoust_id_audio_details(file_path):
    duration,fingerprint = calculate_fingerprints(file_path)
    api_key = ACOUST_ID_TOKEN
    try:
        url = f"""https://api.acoustid.org/v2/lookup?client={api_key}&meta=recordings+releasegroups+compress&duration={duration}&fingerprint={fingerprint}"""
        logger.info(url)
        response = requests.get(url)
        data = response.json()
        logger.info(f"data extracted!!!!")
        return data
    except Exception as error:
        logger.info(f"in get_acoust_id_audio_details: Error: {error}")
        return {"message":"Unable to generate fingerprint for the file" }
