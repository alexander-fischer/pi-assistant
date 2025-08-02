from pia.asr.canary import CanaryAsr
from pia.asr.parakeet import ParakeetAsr
from pia.config import LANGUAGE


class Asr:

    def load(self):
        if LANGUAGE == "en":
            self.model = ParakeetAsr()
        else:
            self.model = CanaryAsr()

        self.model.load()

    def transcribe(self):
        return self.model.transcribe()
