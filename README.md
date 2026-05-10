![Banner](docs/images/codex_plugin.png)

# Codex Forgetful Plugin

Codex-specific plugin packaging for [Forgetful](https://github.com/ScottRBK/forgetful)-powered context gathering.

This repo is separate from the Claude Code plugin repo so Codex-specific plugin structure, marketplace metadata, and setup commands can evolve independently.

## Install

From a clone of this repository:

```bash
codex plugin marketplace add /path/to/codex-forgetful-plugin
```

Then restart Codex, open `/plugins`, install and enable `Forgetful`, start a new thread, and run:

```text
$forgetful-install
```

In the CLI, plugin installation is managed from `/plugins`. The marketplace command only registers this repo as an available marketplace.

## Included Plugin

```text
plugins/forgetful/
  .codex-plugin/plugin.json
  agents/
  hooks.json
  hooks/
  skills/context-gather/
  skills/forgetful-install/
  skills/memory-curate/
```

## What It Does

- Uses `$context-gather` as the core workflow.
- Uses `$forgetful-install` to configure user-specific MCP dependencies.
- Delegates retrieval to a subagent by default so noisy memory and code search does not consume the main agent context.
- Queries Forgetful via the meta-tools pattern.
- Uses local code inspection and Context7 where relevant.
- Includes an optional Stop hook that asks Codex to run `$memory-curate` only when the current git working tree has changes.

## Setup Notes

The plugin does not bundle `.mcp.json` by default. Forgetful MCP setup is user-specific: stdio, `uvx`, local HTTP, remote HTTP, authenticated HTTP, and custom commands are all plausible. Use `$forgetful-install` to check or configure Codex MCP entries for Forgetful and optional Context7.

Stop-hook memory curation is optional and requires Codex plugin hooks to be enabled. See the official [Codex hooks documentation](https://developers.openai.com/codex/hooks) for current setup instructions.

Restart Codex after enabling hooks or reinstalling the plugin.

The Stop hook is deterministic. It skips when curation already ran, when the current directory is not a git repository, or when `git status --porcelain` reports no working-tree changes. When files have changed, it asks Codex to continue with `$memory-curate`, which performs the actual Forgetful duplicate checks and memory writes.
