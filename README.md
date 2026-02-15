# 🐈 nanobot — Coolify Deployment

Deploy [nanobot](https://github.com/HKUDS/nanobot) on [Coolify](https://coolify.io) without forking the upstream repo.

## What's in this repo

```
├── Dockerfile           # Python 3.12 + Node.js 20 + nanobot-ai from PyPI
├── docker-compose.yml   # Coolify-ready compose file
├── entrypoint.sh        # Generates config, starts gateway
├── generate_config.py   # Translates env vars → ~/.nanobot/config.json
├── .env.example         # All available environment variables
└── README.md
```

## Deploy

**Minimum requirements:**
- `OPENROUTER_API_KEY` (required)
- At least one messaging channel enabled (e.g., `TELEGRAM_ENABLED=true` + `TELEGRAM_TOKEN`)

### 1. Fork this repo (optional)

You can use this repo directly, or fork it to your own GitHub/GitLab account if you want to make customizations.

### 2. Create resource in Coolify

1. **Projects → Add Resource → Docker Compose**
2. Select this repo (or your fork if you created one)
3. Coolify will detect the `docker-compose.yml` automatically

### 3. Set environment variables

In Coolify → your resource → **Environment Variables** tab:

| Variable | Required | Example |
|---|---|---|
| `OPENROUTER_API_KEY` | **Yes** | `sk-or-v1-xxx` |
| `NANOBOT_MODEL` | No | `anthropic/claude-sonnet-4-20250514` |
| `BRAVE_SEARCH_API_KEY` | No | `BSA-xxx` |
| `TELEGRAM_ENABLED` | If using Telegram | `true` |
| `TELEGRAM_TOKEN` | If using Telegram | `123456:ABC-DEF...` |
| `TELEGRAM_ALLOW_FROM` | No | `123456789` (comma-separated) |
| `DISCORD_ENABLED` | If using Discord | `true` |
| `DISCORD_TOKEN` | If using Discord | Bot token |
| `DISCORD_ALLOW_FROM` | No | User IDs (comma-separated) |
| `WHATSAPP_ENABLED` | If using WhatsApp | `true` |
| `WHATSAPP_ALLOW_FROM` | No | `+1234567890` (comma-separated) |

**Notes:**
- At least one channel (Telegram/Discord/WhatsApp) must be enabled and configured
- Mark `OPENROUTER_API_KEY`, `TELEGRAM_TOKEN`, `DISCORD_TOKEN`, and `BRAVE_SEARCH_API_KEY` as **Secret**
- `NANOBOT_MODEL` must match [OpenRouter's model ID](https://openrouter.ai/models) exactly (e.g., `anthropic/claude-sonnet-4-20250514`, not `anthropic/claude-sonnet-4`)

### 4. Configure Coolify settings

- **Health check:** set to **None** — the nanobot gateway is a message bus, not an HTTP server
- **Port:** `18790` (optional, exposed in Dockerfile but [does not currently bind an HTTP listener](https://github.com/HKUDS/nanobot/issues/510))
- **Domain:** not required (nanobot communicates via messaging channels, not HTTP)

### 5. Deploy

Click **Deploy**. Watch logs for:
```
✓ Channels enabled: telegram
nanobot — starting gateway...
Telegram bot @YourBot connected
```

## Updating nanobot

The Dockerfile installs the latest `nanobot-ai` from PyPI at build time. To update:

1. **Redeploy** in Coolify (rebuilds the image)

To pin a version, change the Dockerfile:
```dockerfile
RUN pip install --no-cache-dir nanobot-ai==0.1.3.post7
```

## Persistent data

| Volume | Contents |
|---|---|
| `nanobot-data` | Config, memory, sessions, conversation history |
| `nanobot-workspace` | Agent workspace files |

## WhatsApp setup

Only required if `WHATSAPP_ENABLED=true`. WhatsApp requires a manual pairing step after first deploy:

1. Coolify → Terminal tab
2. Run `nanobot channels login`
3. Scan QR code: WhatsApp → Settings → Linked Devices
4. The gateway picks it up automatically

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `No channels enabled` | Channel env vars not set | Set `TELEGRAM_ENABLED=true` (etc) and redeploy |
| Telegram connected but no replies | Wrong model name or bad API key | Check `NANOBOT_MODEL` matches [OpenRouter models](https://openrouter.ai/models) exactly |
| Container restarts in a loop | Health check failing | Set health check to **None** |
| `OPENROUTER_API_KEY` error on start | Env var missing | Add it in Coolify's Environment Variables |
