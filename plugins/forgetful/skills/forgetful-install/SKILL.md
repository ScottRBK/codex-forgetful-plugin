---
name: forgetful-install
description: Install or verify Forgetful dependencies for Codex by interactively configuring Forgetful MCP and optional Context7 MCP. Use when the user asks to install Forgetful, set up Forgetful for Codex, or check Forgetful dependencies.
---

# Forgetful Install

Use this skill to configure the local Codex environment for Forgetful.

Forgetful does not bundle a static `.mcp.json` because Forgetful setup is user-specific. A user may run Forgetful through stdio, `uvx`, a local HTTP server, Docker, a remote server, or an authenticated endpoint. Context7 is optional.

## Workflow

1. Check the current Codex MCP setup.
2. If Forgetful is already configured, report the existing entry and ask before replacing it.
3. If Forgetful is missing, ask which setup the user wants:
   - Standard local stdio setup with `uvx forgetful-ai`.
   - Local or remote HTTP setup.
   - Authenticated HTTP setup using a bearer token environment variable.
   - Custom command setup.
4. Add Forgetful with `codex mcp add`.
5. Ask whether to install Context7 if it is missing.
6. Verify with `codex mcp list` and, when useful, `codex mcp get <name>`.
7. Tell the user to restart Codex if newly added MCP servers are not visible in the active session.

## Commands

Check current MCP servers:

```bash
codex mcp list
```

Standard local Forgetful setup:

```bash
codex mcp add forgetful -- uvx forgetful-ai
```

HTTP Forgetful setup:

```bash
codex mcp add forgetful --url http://localhost:8020/mcp
```

Authenticated HTTP Forgetful setup:

```bash
codex mcp add forgetful --url https://example.com/mcp --bearer-token-env-var FORGETFUL_TOKEN
```

Context7 setup:

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

Inspect configured entries:

```bash
codex mcp get forgetful
codex mcp get context7
```

## Guardrails

- Do not remove or replace existing MCP entries without explicit user approval.
- Do not create memories during install.
- Prefer `codex mcp add` over hand-editing `~/.codex/config.toml`.
- Do not assume Context7 is required; it is recommended for framework documentation lookup.
- If a command fails because it needs network access or writes outside the sandbox, request escalation and rerun the same command.
- If the active session does not show newly configured MCP tools, ask the user to restart Codex.

## Final Status

End with:

```text
Forgetful Install Status:
-------------------------
Forgetful MCP: <configured / missing / unchanged>
Context7 MCP:  <configured / missing / skipped>

Use:
- $context-gather <task>
- $forgetful-install
```
