FROM python:3.12-slim

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
        curl git ca-certificates gnupg && \
    # Node.js 20 (needed for WhatsApp bridge)
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" \
        > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir nanobot-ai

RUN mkdir -p /root/.nanobot

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY generate_config.py /generate_config.py

EXPOSE 18790

ENTRYPOINT ["/entrypoint.sh"]
