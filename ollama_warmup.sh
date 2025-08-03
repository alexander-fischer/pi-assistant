#!/bin/bash

# make sure that models are loaded into RAM before inference
# TODO: adjust to your models
curl http://localhost:11434/api/generate -d '{"model": "gemma3:1b-it-qat", "keep_alive": -1}'
curl http://localhost:11434/api/generate -d '{"model": "hf.co/katanemo/Arch-Function-1.5B.gguf:Q4_K_M", "keep_alive": -1}'
