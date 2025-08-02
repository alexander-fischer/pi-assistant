from nemo.collections.asr.models import EncDecMultiTaskModel
import numpy.typing as npt

from pia.config import LANGUAGE
from pia.asr.transcription import AudioTranscriber


class CanaryAsr:

    def __init__(self) -> None:
        self.model_id = "nvidia/canary-180m-flash"

    def load(self):
        self.canary_model = EncDecMultiTaskModel.from_pretrained(self.model_id)

    def transcribe(self) -> str:
        if not self.canary_model:
            raise Exception("Load model before transcription.")

        def call_asr(audio_np: npt.NDArray):
            transcript = self.canary_model.transcribe(  # type: ignore
                audio=[audio_np],
                batch_size=1,
                source_lang=LANGUAGE,
                target_lang=LANGUAGE,
                pnc="False",
            )
            return transcript[0].text.strip()

        transcriber = AudioTranscriber(call_asr=call_asr)
        transcription = transcriber.transcribe()
        return transcription
