#!/usr/bin/env python3
"""Generate ~/.nanobot/config.json from environment variables."""

import json
import os
import pathlib


def csv_list(val: str) -> list[str]:
    """Split comma-separated string into a list, stripping whitespace."""
    return [v.strip() for v in val.split(",") if v.strip()]


def build_config() -> dict:
    cfg: dict = {}

    # ── Providers ────────────────────────────────────────────────────
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if api_key:
        cfg["providers"] = {"openrouter": {"apiKey": api_key}}

    # ── Agent defaults ───────────────────────────────────────────────
    cfg["agents"] = {
        "defaults": {
            "model": os.environ.get("NANOBOT_MODEL", "anthropic/claude-sonnet-4-20250514"),
        }
    }

    # ── Gateway (bind to 0.0.0.0 so Docker/Coolify can reach it) ───
    cfg["gateway"] = {"host": "0.0.0.0", "port": 18790}

    # ── Web search ───────────────────────────────────────────────────
    brave_key = os.environ.get("BRAVE_SEARCH_API_KEY", "")
    if brave_key:
        cfg["webSearch"] = {"apiKey": brave_key}
        cfg["tools"] = {"web": {"search": {"apiKey": brave_key}}}

    # ── Channels ─────────────────────────────────────────────────────
    channels: dict = {}

    # Telegram
    if os.environ.get("TELEGRAM_ENABLED", "").lower() == "true":
        channels["telegram"] = {
            "enabled": True,
            "token": os.environ.get("TELEGRAM_TOKEN", ""),
            "allowFrom": csv_list(os.environ.get("TELEGRAM_ALLOW_FROM", "")),
        }
    else:
        channels["telegram"] = {"enabled": False}

    # Discord
    if os.environ.get("DISCORD_ENABLED", "").lower() == "true":
        channels["discord"] = {
            "enabled": True,
            "token": os.environ.get("DISCORD_TOKEN", ""),
            "allowFrom": csv_list(os.environ.get("DISCORD_ALLOW_FROM", "")),
        }
    else:
        channels["discord"] = {"enabled": False}

    # WhatsApp
    if os.environ.get("WHATSAPP_ENABLED", "").lower() == "true":
        channels["whatsapp"] = {
            "enabled": True,
            "allowFrom": csv_list(os.environ.get("WHATSAPP_ALLOW_FROM", "")),
        }
    else:
        channels["whatsapp"] = {"enabled": False}

    cfg["channels"] = channels
    return cfg


def main():
    cfg_path = pathlib.Path.home() / ".nanobot" / "config.json"
    cfg_path.parent.mkdir(parents=True, exist_ok=True)

    cfg = build_config()
    cfg_path.write_text(json.dumps(cfg, indent=2))
    print(f"Config written to {cfg_path}")


if __name__ == "__main__":
    main()
