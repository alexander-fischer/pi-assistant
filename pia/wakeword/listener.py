import pyaudio
import numpy as np
from loguru import logger
from pia.wakeword.detector import WakewordDetector


class WakewordListener:
    def __init__(self):
        self.wakeword_detector = WakewordDetector()
        self.chunk = 1280  # number of frames per buffer
        self.rate = 16000  # sampling rate

        # initialize PyAudio and open the input stream
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,  # 16‑bit int samples
            channels=1,  # mono
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

    def listen(self) -> bool:
        self.wakeword_detector.reset()
        logger.info("Listening for wakeword...")

        while True:
            try:
                buf = self.stream.read(self.chunk, exception_on_overflow=False)
            except IOError as e:
                logger.warning(f"Stream read error: {e}")
                continue

            # convert raw bytes to numpy array of int16 samples
            pcm = np.frombuffer(buf, dtype=np.int16)
            if self.wakeword_detector.check(pcm):
                logger.info("Wakeword detected!")
                return True

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
