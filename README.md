# Codex Forgetful Plugin

Codex-specific plugin packaging for Forgetful-powered context gathering.

This repo is separate from the Claude Code `context-hub-plugin` repo so Codex-specific plugin structure, marketplace metadata, and setup commands can evolve independently.

## Install

From a clone of this repository:

```bash
codex plugin marketplace add /path/to/codex-forgetful-plugin
```

Then enable the `context-hub` plugin in Codex and run:

```text
/context-hub-install
```

## Included Plugin

```text
plugins/context-hub/
  .codex-plugin/plugin.json
  commands/
  agents/
  skills/context-gather/
```

## What It Does

- Uses `$context-gather` as the core workflow.
- Treats `/context_gather <task>` as a thin command shim for that skill.
- Delegates retrieval to a subagent by default so noisy memory and code search does not consume the main agent context.
- Queries Forgetful via the meta-tools pattern.
- Uses local code inspection and Context7 where relevant.

## Setup Notes

The plugin does not bundle `.mcp.json` by default. Use `/context-hub-install` to check or configure Codex MCP entries for Forgetful and Context7.
