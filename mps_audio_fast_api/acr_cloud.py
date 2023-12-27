"""
This is a demo program which implements ACRCloud Identify Protocol V1 with the third party library "requests".
We recomment you implement your own app with "requests" too.
You can install this python library by:
1) sudo easy_install requests
2) sudo pip install requests
"""

import base64
import hashlib
import hmac
import os
import sys
import time
from mps_audio_fast_api.config import HOST, ACCESS_KEY, ACCESS_SECRET
import requests



requrl = f"https://{HOST}/v1/identify"
http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method + "\n" + http_uri + "\n" + ACCESS_KEY + "\n" + data_type + "\n" + signature_version + "\n" + str(
    timestamp)

sign = base64.b64encode(hmac.new(ACCESS_SECRET.encode('ascii'), string_to_sign.encode('ascii'),
                                 digestmod=hashlib.sha1).digest()).decode('ascii')


def acr_cloud_identify_audio(audio_file_path):
    sample_bytes = os.path.getsize(audio_file_path)
    file_extension = audio_file_path.split(".")[1]
    try:
        if file_extension == "wav":
            file_type = "audio/wav"
        elif file_extension == "mp3":
            file_type = "audio/mpeg"
        elif file_extension == "aac":
            file_type = "audio/aac"

        files = [
            ('sample', (audio_file_path, open(audio_file_path, 'rb'),file_type))
        ]
        data = {'access_key': ACCESS_KEY,
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': data_type,
            "signature_version": signature_version}

        r = requests.post(requrl, files=files, data=data)
        r.encoding = "utf-8"
        return r.text
    except Exception as error:
        return error
