# from pydub import AudioSegment
# import chromaprint
import requests
# import acoustid
# import commands
import re
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
        print(output)
        return output
        # if 'fingerprint: ' in result.stderr:
        #     fingerprint = result.stderr.split('fingerprint: ')[1].strip()
        #     logger.info(f"Fingerprint generated for {file_path}")
        #     print(f"Fingerprint generated for {file_path}")
        #     return fingerprint
        # else:
        #     logger.error("Fingerprint not found in stderr.")
        #     print("Fingerprint not found in stderr.")
        #     return None

    except subprocess.CalledProcessError as error:
        logger.error(f"Error generating fingerprint: {error}")
        print(f"Error generating fingerprint: {error}")
        return None




def calculate_fingerprints(filename):
    sample_time = 5000
    command = ['fpcalc', filename]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = str(result.stdout)
        duration_index = data.find('DURATION=') + len('DURATION=')
        duration_end_index = data.find('\n', duration_index)
        duration = int(data[duration_index:duration_end_index])
        fingerprint_index = data.find('FINGERPRINT=') + len('FINGERPRINT=')
        fingerprint = data[fingerprint_index:].strip()
        print(fingerprint)
        print(duration)
        return duration, fingerprint

    except subprocess.CalledProcessError as e:
        print(f"Error running fpcalc: {e}")
        return None


# def generate_fingerprint(file_path):
#     try:
#         duration, fp = acoustid.fingerprint_file(file_path)
#         fingerprint = acoustid.fingerprint_encode(fp)
#         logger.info(f"Fingerprint Generated for {file_path}")
#         print(f"Fingerprint Generated for {file_path}")
#         return fingerprint
#     except Exception as error:
#         logger.info(f"Error generating fingerprint: {error}")
#         return f"Error: {error}"



def get_duration(file_path):
    try:
        result = subprocess.run(['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
                                capture_output=True, text=True)
        duration = float(result.stdout.strip())
        print(f"duration: {duration}")
        return duration
    except Exception as error:
        logger.info(f"Error getting audio duration: {error}")
        return(f"Error: {error}")


def get_acoust_id_audio_details(file_path):
    duration,fingerprint = calculate_fingerprints(file_path)
    api_key = ACOUST_ID_TOKEN
    try:
        url = f"""https://api.acoustid.org/v2/lookup?client={api_key}&duration={duration}&fingerprint={fingerprint}"""
        print(url)
        response = requests.get(url)
        data = response.json()
        print(f"response data: {data}")
        return data
    except Exception as error:
        print(f"Error: {error}")
        logger.info(f"Error: {error}")
        return error
