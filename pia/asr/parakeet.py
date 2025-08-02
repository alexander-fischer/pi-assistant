import onnx_asr
import numpy.typing as npt
from pia.asr.transcription import AudioTranscriber


class ParakeetAsr:

    def __init__(self) -> None:
        self.model_id = "nemo-parakeet-tdt-0.6b-v2"
        self.quantization = "int8"

    def load(self):
        self.canary_model = onnx_asr.load_model(
            self.model_id, quantization=self.quantization
        )

    def transcribe(self) -> str:
        if not self.canary_model:
            raise Exception("Load model before transcription.")

        def call_asr(audio_np: npt.NDArray):
            transcript = self.canary_model.recognize(audio_np)
            return transcript.strip()

        transcriber = AudioTranscriber(call_asr=call_asr)
        transcription = transcriber.transcribe()
        return transcription
