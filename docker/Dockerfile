FROM node:20-slim

# ── Metadata ──
LABEL maintainer="pedrormc"
LABEL description="Claude Code sandboxed dev container with toolkit pre-installed"

# ── Build args ──
ARG CLAUDE_CODE_VERSION=latest
ARG USERNAME=coder
ARG USER_UID=1000
ARG USER_GID=1000

# ── System packages ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    jq \
    fzf \
    vim-tiny \
    nano \
    ripgrep \
    iptables \
    ipset \
    iproute2 \
    dnsutils \
    ca-certificates \
    sudo \
    openssh-client \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# ── Create non-root user ──
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME} \
    && echo "${USERNAME} ALL=(root) NOPASSWD: /usr/sbin/iptables,/usr/sbin/ip6tables,/usr/sbin/ipset" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# ── Install Claude Code ──
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
    && npm cache clean --force

# ── Setup directories ──
RUN mkdir -p /home/${USERNAME}/.claude \
    /workspace \
    /commandhistory \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.claude \
    /workspace \
    /commandhistory

# ── Copy toolkit ──
COPY --chown=${USERNAME}:${USERNAME} agents/ /home/${USERNAME}/.claude/agents/
COPY --chown=${USERNAME}:${USERNAME} rules/ /home/${USERNAME}/.claude/rules/
COPY --chown=${USERNAME}:${USERNAME} skills/ /home/${USERNAME}/.claude/skills/
COPY --chown=${USERNAME}:${USERNAME} scripts/ /home/${USERNAME}/.claude/scripts/
COPY --chown=${USERNAME}:${USERNAME} config/settings.json /home/${USERNAME}/.claude/settings.json
COPY --chown=${USERNAME}:${USERNAME} config/settings.local.json /home/${USERNAME}/.claude/settings.local.json
COPY --chown=${USERNAME}:${USERNAME} statusline.sh /home/${USERNAME}/.claude/statusline.sh
COPY --chown=${USERNAME}:${USERNAME} plugins/ /home/${USERNAME}/.claude/plugins/
COPY --chown=${USERNAME}:${USERNAME} teams/ /home/${USERNAME}/.claude/teams/
COPY --chown=${USERNAME}:${USERNAME} scheduled-tasks/ /home/${USERNAME}/.claude/scheduled-tasks/
COPY --chown=${USERNAME}:${USERNAME} templates/ /home/${USERNAME}/.claude/templates/

# ── Create skills/learned ──
RUN mkdir -p /home/${USERNAME}/.claude/skills/learned \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.claude

# ── Chmod scripts ──
RUN chmod +x /home/${USERNAME}/.claude/statusline.sh \
    && chmod +x /home/${USERNAME}/.claude/scripts/*.js 2>/dev/null || true

# ── Copy entrypoint and firewall ──
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY docker/init-firewall.sh /usr/local/bin/init-firewall.sh
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/init-firewall.sh

# ── Environment ──
ENV CLAUDE_CONFIG_DIR=/home/${USERNAME}/.claude
ENV NODE_OPTIONS=--max-old-space-size=4096
ENV HISTFILE=/commandhistory/.bash_history
ENV TERM=xterm-256color

# ── Switch to non-root ──
USER ${USERNAME}
WORKDIR /workspace

ENTRYPOINT ["entrypoint.sh"]
CMD ["bash"]
