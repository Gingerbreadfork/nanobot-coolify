#!/bin/bash
set -e

echo "══════════════════════════════════════════════"
echo "  nanobot — generating config..."
echo "══════════════════════════════════════════════"

python3 /generate_config.py

echo "══════════════════════════════════════════════"
echo "  nanobot — starting gateway..."
echo "══════════════════════════════════════════════"

exec nanobot gateway
