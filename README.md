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

### 1. Push this repo to GitHub/GitLab

```bash
git init && git add -A && git commit -m "init"
git remote add origin git@github.com:YOU/nanobot-coolify.git
git push -u origin main
```

### 2. Create resource in Coolify

1. **Projects → Add Resource → Docker Compose**
2. Select your Git repo
3. Coolify will detect the `docker-compose.yml` automatically

### 3. Set environment variables

In Coolify → your resource → **Environment Variables** tab:

| Variable | Required | Example |
|---|---|---|
| `OPENROUTER_API_KEY` | **Yes** | `sk-or-v1-xxx` |
| `NANOBOT_MODEL` | No | `anthropic/claude-sonnet-4-20250514` |
| `BRAVE_SEARCH_API_KEY` | No | `BSA-xxx` |
| `TELEGRAM_ENABLED` | No | `true` |
| `TELEGRAM_TOKEN` | No | `123456:ABC-DEF...` |
| `TELEGRAM_ALLOW_FROM` | No | `123456789` (comma-separated) |
| `DISCORD_ENABLED` | No | `true` |
| `DISCORD_TOKEN` | No | Bot token |
| `DISCORD_ALLOW_FROM` | No | User IDs (comma-separated) |
| `WHATSAPP_ENABLED` | No | `true` |
| `WHATSAPP_ALLOW_FROM` | No | `+1234567890` (comma-separated) |

Mark `OPENROUTER_API_KEY`, `TELEGRAM_TOKEN`, `DISCORD_TOKEN`, and `BRAVE_SEARCH_API_KEY` as **Secret**.

### 4. Configure Coolify settings

- **Port:** `18790`
- **Domain:** e.g. `nanobot.example.com`
- **Health check:** set to **None** — the nanobot gateway is a message bus, not an HTTP server. Port 18790 is exposed in the Dockerfile but [does not currently bind an HTTP listener](https://github.com/HKUDS/nanobot/issues/510).

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

WhatsApp requires a manual pairing step after first deploy:

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

## Model name gotcha

The `NANOBOT_MODEL` value must match OpenRouter's model ID exactly. Examples:

- `anthropic/claude-sonnet-4-20250514` ✅
- `anthropic/claude-sonnet-4` ❌ (won't resolve)
- `minimax/minimax-m2` ✅

Check https://openrouter.ai/models for the exact string.
