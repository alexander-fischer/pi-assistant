from dotenv import load_dotenv
import os

load_dotenv()

# relevant for prompts and tts
LANGUAGE = os.getenv("LANGUAGE", "en")

# max words to use in wikipedia
MAX_WIKIPEDIA_CONTENT_LENGTH = int(os.getenv("MAX_WIKIPEDIA_CONTENT_LENGTH", 16000))

# relevant for smart home
HUE_IP_ADDRESS = os.getenv("HUE_IP_ADDRESS", "")
HUE_API_KEY = os.getenv("HUE_API_KEY", "")

# relevant for inference
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1")  # default to Ollama
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_KEEP_ALIVE = os.getenv("LLM_KEEP_ALIVE", "24h")
TOOL_MODEL = os.getenv("TOOL_MODEL", "hf.co/LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M")
TOOL_MODEL_TEMPERATURE = float(os.getenv("TOOL_MODEL_TEMPERATURE", 0.0))
ANSWER_MODEL = os.getenv("ANSWER_MODEL", "hf.co/LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M")
ANSWER_MODEL_TEMPERATURE = float(os.getenv("ANSWER_MODEL_TEMPERATURE", 0.3))

# wakeword settings
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
WAKEWORD_MODEL = os.getenv("WAKEWORD_MODEL", "model/wakeword/hey_jarvis_v0.1.onnx")
WAKEWORD_THRESHOLD = float(os.getenv("WAKEWORD_THRESHOLD", 0.5))

# speech to text settings
PHRASE_TIME_LIMIT = float(os.getenv("PHRASE_TIME_LIMIT", 7.0))
TRANSCRIPTION_TIMEOUT = float(os.getenv("TRANSCRIPTION_TIMEOUT", 10.0))

# text to speech settings
TTS_ENGINE = os.getenv("TTS_ENGINE", "piper")
TTS_DE_MODEL = os.getenv("TTS_DE_MODEL", "model/piper/de_DE-thorsten-high.onnx")
TTS_EN_MODEL = os.getenv("TTS_EN_MODEL", "model/piper/en_GB-alan-medium.onnx")
DEVICE_SAMPLE_RATE = int(os.getenv("DEVICE_SAMPLE_RATE", 48000))
