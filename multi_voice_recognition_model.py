import torch
from pyannote.audio import Pipeline
from config import ACCESS_TOKEN
from log import setup_logger

logger = setup_logger(__name__)

def get_multi_voice_output(audio_file):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=ACCESS_TOKEN)
    pipeline.to(torch.device("cuda"))
    diarization = pipeline(audio_file)
    speaker_list = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        logger.info(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        speaker_list.append(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    return speaker_list
