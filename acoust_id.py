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
    command = ['fpcalc', '-raw', '-length', str(sample_time), filename]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        fpcalc_out = result.stdout
        fingerprint_index = fpcalc_out.find('FINGERPRINT=') + 12
        fingerprints = list(map(int, fpcalc_out[fingerprint_index:].split(',')))
        print(f"Fingerprints from fpcalc: {fingerprints}")
        return fingerprints

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
    data_dict = dict()
    fingerprint = calculate_fingerprints(file_path)
    # fingerprint= generate_fingerprint(file_path)
    duration = get_duration(file_path)
    api_key = ACOUST_ID_TOKEN
    try:
        url = f"""https://api.acoustid.org/v2/lookup?client={api_key}&duration={duration}&fingerprint={fingerprint}"""
        print(f"url: {url}")
        response = requests.get(url)
        data = response.json()
        print(f"response data: {data}")
        if 'results' in data and data['results']:
            result = data['results'][0]
            recording_id = result['id']
            title = result['recordings'][0]['title']
            artist = result['recordings'][0]['artists'][0]['name']
            data_dict["Recording ID"] = recording_id
            data_dict["Title"] = title
            data_dict["Artist"] = artist
            data_dict["jsondata"] = response.json()
            logger.info(f"Recording ID: {recording_id}")
            logger.info(f"Title: {title}")
            logger.info(f"Artist: {artist}")
            print(f"Recording ID: {recording_id}")
            print(f"Title: {title}")
            print(f"Artist: {artist}")
            return data_dict
        else:
            logger.info("No matching result found.")
            print("No matching result found.")
            return {f"Else block: {data}"}
    except Exception as error:
        print(f"Error: {error}")
        logger.info(f"Error: {error}")
        return error
