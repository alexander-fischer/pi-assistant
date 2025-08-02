import signal
import sys
from openai import Stream
import typer
from rich.prompt import Prompt
from loguru import logger
from rich import print
import i18n
from pia.asr.main import Asr
from pia.config import LANGUAGE
from pia.tts.main import Tts
from pia.workflow import call_assistant
from pia.wakeword.listener import WakewordListener

wakeword_listener = WakewordListener()


# Handle exit
def signal_handler(sig, frame):
    print(f"\n\n[white]{i18n.t('bye')}[/white]")
    wakeword_listener.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def run_audio_mode():
    # setup audio
    asr = Asr()
    asr.load()
    tts = Tts()
    tts.load()

    while True:
        print(f"[white]{i18n.t('assistant-listening')}[/white]\n")
        wakeword_detected = wakeword_listener.listen()
        if not wakeword_detected:
            break
        # make sure the user knows that wake word was detected
        tts.text_to_speech(i18n.t("assistant-reaction"), wait=False)

        instruction = asr.transcribe()
        if not instruction.strip():
            continue

        print(f"{i18n.t('you')}: {instruction}\n")
        answer = call_assistant(instruction=instruction, audio_mode=True)

        assert isinstance(answer, str)
        tts.text_to_speech(answer)


def run_terminal_mode():
    print(f"[white]{i18n.t('assistant-greeting')}[/white]\n")

    while True:
        instruction = Prompt.ask(i18n.t("you"))
        answer = call_assistant(instruction=instruction, audio_mode=False)

        assert isinstance(answer, Stream)
        is_first_iter = True
        for chunk in answer:
            delta = chunk.choices[0].delta
            chunk_content = delta.content
            if not chunk_content:
                continue

            if is_first_iter:
                chunk_content = f"\n{i18n.t('assistant')}: {chunk_content}"
                is_first_iter = False

            print(f"[white]{chunk_content}[/white]", end="", flush=True)
        print("\n")


def run(audio_mode: bool):
    if audio_mode:
        run_audio_mode()
    else:
        run_terminal_mode()


@logger.catch
def cli(
    audio: bool = False,
    verbose: bool = False,
):
    """Client tool for app.

    Args:
        audio: Run audio mode for hands free question and answers.
        verbose:
    """
    logger.remove()
    if verbose:
        logger.add(sys.stdout, level="DEBUG")

    i18n.load_path.append("i18n/")
    i18n.set("locale", LANGUAGE)
    i18n.set("filename_format", "{locale}.{format}")

    run(audio_mode=audio)


def start_cli():
    typer.run(cli)
