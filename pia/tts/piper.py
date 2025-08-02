from loguru import logger
from piper import PiperVoice
import sounddevice as sd
import numpy as np
import librosa
from pia.config import DEVICE_SAMPLE_RATE, LANGUAGE, TTS_DE_MODEL, TTS_EN_MODEL


class PiperTts:
    def __init__(self) -> None:
        if LANGUAGE == "de":
            self.voice = PiperVoice.load(TTS_DE_MODEL)
        else:
            self.voice = PiperVoice.load(TTS_EN_MODEL)

    def text_to_speech(self, text: str, wait: bool = True):
        logger.info("Generating audio…")
        audio = self.voice.synthesize(text)
        logger.info(f"Audio chunks generated")

        for sequence in audio:
            resampled_sequence = self._resample(
                sequence.audio_float_array, sequence.sample_rate
            )
            sd.play(resampled_sequence, DEVICE_SAMPLE_RATE)
            if wait:
                sd.wait()

    def _resample(self, chunk: np.ndarray, sr: int) -> np.ndarray:
        if sr != DEVICE_SAMPLE_RATE:
            mono = chunk if chunk.ndim == 1 else chunk.mean(axis=1)
            return librosa.resample(mono, orig_sr=sr, target_sr=DEVICE_SAMPLE_RATE)
        return chunk
