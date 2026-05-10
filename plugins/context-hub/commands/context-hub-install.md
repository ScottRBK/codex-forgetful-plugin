---
description: Install and configure Context Hub dependencies for Codex
argument-hint: [standard|http URL|check]
allowed-tools: [Bash, Read, Grep]
---

# Context Hub Install

Install and configure Context Hub's Codex dependencies: Forgetful MCP and optional Context7 documentation support.

The user invoked this command with:

$ARGUMENTS

## Step 1: Check Current Codex Setup

Run:

```bash
codex mcp list
```

Look for:

- `forgetful` or `forgetful_cloud`
- `context7`

Also inspect `~/.codex/config.toml` if command output is unclear.

## Step 2: Configure Forgetful MCP

If a Forgetful MCP server is already configured, report it and ask before replacing it.

### Standard Local Setup

Use this when the user wants local SQLite storage and zero extra service management:

```bash
codex mcp add forgetful -- uvx forgetful-ai
```

Verify with:

```bash
codex mcp get forgetful
```

### HTTP Setup

Use this when the user runs Forgetful as Docker, remote HTTP, or staging/cloud:

```bash
codex mcp add forgetful --url http://localhost:8020/mcp
```

For authenticated HTTP servers, use Codex's bearer token option:

```bash
codex mcp add forgetful --url https://example.com/mcp --bearer-token-env-var FORGETFUL_TOKEN
```

## Step 3: Check Context7

Context7 is recommended, not required. If missing, explain that `$context-gather` will still work with Forgetful and local code, but framework documentation lookup may be unavailable.

Expected Codex MCP setup:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

## Step 4: Report Status

Report:

```text
Context Hub Install Status:
---------------------------
Forgetful MCP:  Configured / Not configured
Context7 MCP:   Configured / Not configured

Commands:
- /context_gather <task>
- /context-hub-install

Skill:
- $context-gather
```

## Guardrails

- Do not remove or replace existing MCP entries without explicit user approval.
- Do not create memories during install.
- Prefer `codex mcp add` over hand-editing `~/.codex/config.toml`.
- For custom Forgetful settings, consult the current Forgetful configuration docs before composing commands.
