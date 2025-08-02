# pi-assistant

**pi-assistant** is a tool-calling assistant designed for the Raspberry Pi. It can answer knowledge questions, provide weather updates, and control your smart home devices using small language models, wake word detection, automatic speech recognition (ASR), and text-to-speech (TTS).
_Blog article coming soon!_

> **Note:** Currently, only tested on Raspberry Pi 5 (16GB RAM).

---

## Features

-   Ask for weather or general knowledge
-   Control your smart home (e.g., Philips Hue)
-   Wake word detection (“Hey Jarvis”)
-   ASR and TTS integration

---

## Setup

### Philips Hue Integration

For connecting with Philips Hue, please follow the official setup instructions:
[Philips Hue Developer Getting Started](https://developers.meethue.com/develop/get-started-2/)

### Installation

Run the provided setup script to install dependencies:

```bash
./setup_pi.sh
```

> **Note:** Sometimes you may need to run the script twice and restart the Raspberry Pi terminal for all dependencies to be installed correctly.

---

## Usage

### Terminal Mode

Run the assistant in text mode:

```bash
poetry run pia
```

### Audio Mode (ASR and TTS)

Enable voice input/output with:

```bash
poetry run pia --audio
```

_Say “Hey Jarvis” to activate the assistant._

### Debug Mode

For verbose logging, use:

```bash
poetry run pia --verbose
```
