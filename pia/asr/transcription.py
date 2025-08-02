from loguru import logger
import speech_recognition as sr
import numpy as np
from typing import Callable
import numpy.typing as npt

from pia.config import PHRASE_TIME_LIMIT, TRANSCRIPTION_TIMEOUT


class AudioTranscriber:
    def __init__(
        self,
        call_asr: Callable[[npt.NDArray[np.float32]], str],
    ) -> None:
        self.call_asr = call_asr

        # audio paramters for transcription
        self.phrase_time_limit = PHRASE_TIME_LIMIT
        self.transcription_timeout = TRANSCRIPTION_TIMEOUT

        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.chunk = 1280
        self.rate = 16000
        self.source = sr.Microphone(sample_rate=self.rate, chunk_size=self.chunk)

    def transcribe(self) -> str:
        logger.info("Listening for instruction...")

        with self.source as src:
            self.recognizer.adjust_for_ambient_noise(src)

            while True:
                try:
                    user_audio = self.recognizer.listen(
                        src,
                        timeout=self.transcription_timeout,
                        phrase_time_limit=self.phrase_time_limit,
                    )
                except Exception as e:
                    logger.error(e)
                    return ""

                logger.info("Transcription started...")
                user_np = (
                    np.frombuffer(user_audio.get_raw_data(), dtype=np.int16).astype(  # type: ignore
                        np.float32
                    )
                    / 32768.0
                )
                transcription = self.call_asr(user_np)
                logger.info(f"Transcription: {transcription}")
                return transcription
