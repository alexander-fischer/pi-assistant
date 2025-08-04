import asyncio
import hashlib
import threading
from typing import Optional

from loguru import logger
import numpy as np
import onnxruntime
import sounddevice as sd
import librosa
import re
import os
from kokoro_onnx import Kokoro
from pia.config import DEVICE_SAMPLE_RATE


class KokoroTts:
    def __init__(self) -> None:
        self.kokoro = Kokoro(
            "model/kokoro/kokoro-v1.0.int8.onnx",
            "model/kokoro/voices-v1.0.bin",
        )
        # make kokoro use all compute cores
        num_threads = os.cpu_count() or 1
        logger.info(f"Num threads: {num_threads}")
        sess_opt = onnxruntime.SessionOptions()
        sess_opt.intra_op_num_threads = num_threads
        sess_opt.inter_op_num_threads = num_threads
        sess_opt.graph_optimization_level = (
            onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        )
        self.kokoro.sess._sess_options = sess_opt

        self._memory_cache: dict[str, np.ndarray] = {}

    def _text_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    def _resample(self, chunk: np.ndarray, sr: int) -> np.ndarray:
        if sr != DEVICE_SAMPLE_RATE:
            mono = chunk if chunk.ndim == 1 else chunk.mean(axis=1)
            return librosa.resample(mono, orig_sr=sr, target_sr=DEVICE_SAMPLE_RATE)
        return chunk

    def _split_text(self, text: str) -> list[str]:
        pattern = r"(?<=[,\.!?])\s+"
        return [seg for seg in re.split(pattern, text) if seg.strip()]

    async def _generate_audio_and_play(self, text: str, key: str):
        logger.info("Generating audio…")

        batches = self._split_text(text)
        voice, speed, lang = "bm_lewis", 1.0, "en-gb"

        queue: asyncio.Queue[Optional[np.ndarray]] = asyncio.Queue()
        chunks: list[np.ndarray] = []

        async def producer() -> None:
            loop = asyncio.get_running_loop()
            for i, batch in enumerate(batches):
                # Generate and enqueue chunk directly
                chunk, sr = await loop.run_in_executor(None, kokoro.create, batch, voice, speed, lang)  # type: ignore
                chunk = self._resample(chunk, sr)
                logger.info(f"Audio chunk {i} generated")

                chunks.append(chunk)
                queue.put_nowait(chunk)

            # Signal completion
            queue.put_nowait(None)

        async def consumer() -> None:
            out = sd.RawOutputStream(
                samplerate=DEVICE_SAMPLE_RATE,
                channels=1,
                dtype="int16",
                blocksize=DEVICE_SAMPLE_RATE // 10,
                latency="low",
            )
            out.start()

            chunk_nr = 0
            while True:
                chunk = await queue.get()
                if chunk is None:
                    break
                logger.info(f"Play audio chunk {chunk_nr}")
                pcm = np.clip(chunk * 32767, -32768, 32767).astype(np.int16, copy=False)
                out.write(pcm.tobytes())
                chunk_nr += 1

            out.stop()
            sd.wait()
            out.close()

        # Run both tasks concurrently
        await asyncio.gather(producer(), consumer())

        # Cache the full audio
        audio = np.concatenate(chunks, axis=0).astype(np.float32)
        self._memory_cache[key] = audio

    def _play_audio(self, audio: np.ndarray, wait: bool):
        sd.play(audio, DEVICE_SAMPLE_RATE)
        if wait:
            sd.wait()

    def _run_audio_generation(self, text: str, key: str, wait: bool):
        def audio_job():
            asyncio.run(self._generate_audio_and_play(text, key))

        if wait:
            audio_job()
        else:
            thread = threading.Thread(target=audio_job, daemon=True)
            thread.start()

    def text_to_speech(self, text: str, wait: bool = True):
        """Generate audio of the text and play it.

        Args:
            text: Input text that should be played.
            wait: Stops until audio was played.
        """

        # check if text was already cached
        key = self._text_hash(text)
        if key in self._memory_cache:
            logger.info("Cache hit")
            audio = self._memory_cache[key]
            self._play_audio(audio, wait)
        else:
            self._run_audio_generation(text, key, wait)
