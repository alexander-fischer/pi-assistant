#!/bin/bash

sudo apt update
sudo apt upgrade -y

# pipx
sudo apt install pipx -y
pipx ensurepath

# poetry
pipx install poetry
poetry config virtualenvs.in-project true
poetry install

# ollama
# TODO: change to your model hosting if needed
curl -fsSL https://ollama.com/install.sh | sh
ollama pull hf.co/katanemo/Arch-Function-1.5B.gguf:Q4_K_M
ollama pull gemma3:1b-it-qat
./ollama_warmup.sh

# piper
mkdir -p model/piper
cd model/piper
curl -L -o en_GB-alan-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/en_GB-alan-medium.onnx?download=true"
curl -L -o en_GB-alan-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json?download=true"
cd ..

# wakeword
mkdir -p ./wakeword
cd ./wakeword
curl -L -o hey_jarvis_v0.1.onnx \
  "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/hey_jarvis_v0.1.onnx"
cd ../..
