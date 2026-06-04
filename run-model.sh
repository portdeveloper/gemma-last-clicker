#!/usr/bin/env bash
# Launch Gemma 4 12B locally via llama.cpp (Metal).
# Chat UI + OpenAI-compatible API at http://127.0.0.1:8080
# Thinking mode is on by default. If a reply comes back empty, raise the token
# limit (thinking ate the budget). For snappier replies, pass enable_thinking:false.
set -euo pipefail

SERVER="$HOME/llama.cpp-bin/extracted/llama-b9518/llama-server"
MODEL="$HOME/models/gemma-4-12b-it/gemma-4-12b-it-UD-Q4_K_XL.gguf"

DYLD_LIBRARY_PATH="$(dirname "$SERVER")" exec "$SERVER" \
  -m "$MODEL" \
  --host 127.0.0.1 --port 8080 \
  -c 16384 -ngl 99 \
  --temp 1.0 --top-p 0.95 --top-k 64 \
  --jinja
