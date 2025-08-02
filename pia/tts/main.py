from pia.config import LANGUAGE, TTS_ENGINE
from pia.tts.kokoro import KokoroTts
from pia.tts.piper import PiperTts


class Tts:

    def load(self):
        if LANGUAGE == "de" or TTS_ENGINE == "piper":
            self.model = PiperTts()
        else:
            self.model = KokoroTts()

    def text_to_speech(self, text: str, wait: bool = True):
        self.model.text_to_speech(text=text, wait=wait)
