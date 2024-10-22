"""
The code uses pyannote from Hugging Face to seperate audio files into different
segment later it is fed to Machine Learning Model to identify the human voices
"""
import os
from collections import Counter
from pyannote.audio import Pipeline
from config import ACCESS_TOKEN
from log import setup_logger
import librosa
import soundfile as sf
from voice_recognition_model import identify_the_audio
from child_voice_recognition_model import identify_the_child_audio

logger = setup_logger(__name__)


def get_multi_voice_output(audio_file):
    """
    Args: audio_file (audio file path)
    Output: male count, female count
    """
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=ACCESS_TOKEN)
    diarization = pipeline(audio_file)
    y, sr = librosa.load(audio_file)
    speaker_list = []
    file_name_1 = "extracted_audio_"
    file_name_2 = ".wav"
    unique_speakers = set()
    i = 0
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_time = turn.start
        end_time = turn.end
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        start_sample = int(start_sample)
        end_sample = int(end_sample)
        extracted_audio = y[start_sample:end_sample]
        extracted_audio_file = f"{file_name_1}{i}{file_name_2}"
        sf.write(extracted_audio_file, extracted_audio, sr)
        result = identify_the_audio(extracted_audio_file)
        child_result = identify_the_child_audio(extracted_audio_file)
        if speaker not in unique_speakers:
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker} Identified Speakers: {result}")
            unique_speakers.add(speaker)
            speaker_list.append(result)
        if speaker not in unique_speakers:
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker} Identified Child Speakers: {child_result}")
            unique_speakers.add(speaker)
            speaker_list.append(child_result)
        os.remove(extracted_audio_file)
        i += 1
    gender_counts = Counter(speaker_list)
    male_count = gender_counts.get("male", 0)
    female_count = gender_counts.get("female", 0)
    child_count = gender_counts.get("child",0)
    Counts = {"male_count": f"{male_count}",
              "female_count": f"{female_count}",
              "child_count": f"{child_count}"}
    return Counts
