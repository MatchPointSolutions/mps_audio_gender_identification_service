#import torch
from pyannote.audio import Pipeline
from config import ACCESS_TOKEN
from log import setup_logger
import librosa
from voice_recognition_model import identify_the_audio

logger = setup_logger(__name__)

def get_multi_voice_output(audio_file):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=ACCESS_TOKEN)
    #pipeline.to(torch.device("cuda"))
    diarization = pipeline(audio_file)
    # Load audio file
    y, sr = librosa.load(audio_file)
    speaker_list = [], file_name_1="extracted_audio", file_name_2 =".wav", i=0
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        logger.info(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        speaker_list.append(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        start_sample = int(turn.start:.1f * sr)
        end_sample = int(turn.end:.1f * sr)
        extracted_audio = y[start_sample:end_sample]
        # Save extracted audio
        librosa.save(file_name_1+i+file_name_2, extracted_audio, sr)
        result = identify_the_audio(file_name_1+i+file_name_2)
        i=i+1
    return speaker_list.append(result)
