#import torch
from pyannote.audio import Pipeline
from config import ACCESS_TOKEN
from log import setup_logger
import librosa
import soundfile as sf
from voice_recognition_model import identify_the_audio

logger = setup_logger(__name__)


def get_multi_voice_output(audio_file):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=ACCESS_TOKEN)
    diarization = pipeline(audio_file)
    y, sr = librosa.load(audio_file)
    speaker_list = []
    file_name_1 = "extracted_audio_"
    file_name_2 = ".wav"

    i = 0
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_time = turn.start
        end_time = turn.end
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        start_sample = int(start_sample)
        end_sample = int(end_sample)
        extracted_audio = y[start_sample:end_sample]
        extracted_audio_file = f"{file_name_1}{i}{file_name_2}.wav"
        sf.write(extracted_audio_file, extracted_audio, sr)
        result = identify_the_audio(extracted_audio_file)
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker} Identified Speakers: {result}")
        speaker_list.extend(result)
        i += 1

    return speaker_list
