# Forgetful for Codex

Forgetful packages Scottesh's context-gather workflow for Codex.

The plugin focuses on three Codex skills:

- `$context-gather`: gather implementation context before planning or coding.
- `$forgetful-install`: configure Forgetful MCP and optional Context7 MCP for the local Codex environment.
- `$memory-curate`: save durable decisions, patterns, preferences, and project knowledge to Forgetful.

## What It Does

- Delegates retrieval to a subagent so noisy memory, documentation, and code search do not flood the main agent context.
- Searches Forgetful memory across all projects by default.
- Follows linked memories, documents, code artifacts, and skills when they clarify the task.
- Inspects local code with targeted `rg` and file reads.
- Uses Context7 for library and framework guidance when relevant.
- Uses web search only as a fallback for current authoritative context.
- Includes a Stop hook that can ask Codex to run `$memory-curate` after a turn.

## Skills

- `$context-gather <task>`: gather a focused implementation brief before planning or editing.
- `$forgetful-install`: check and configure Codex dependencies for Forgetful and Context7.
- `$memory-curate`: curate durable knowledge from the completed turn into Forgetful.

## Hooks

The plugin includes root-level `hooks.json` with a `Stop` hook. The hook is intentionally small and deterministic: it checks whether curation already ran for the stop event, then asks Codex to continue with `$memory-curate`.

Codex plugin hooks require the feature flag:

```bash
codex features enable plugin_hooks
```

## Install From A Cloned Repo

From a clone of this repository:

```bash
codex plugin marketplace add /path/to/codex-forgetful-plugin
```

Then restart Codex, open `/plugins`, install and enable `Forgetful`, start a new thread, and run:

```text
$forgetful-install
```

Restart Codex again after enabling `plugin_hooks` or reinstalling the plugin so hook registration is loaded fresh.

## Dependencies

Forgetful expects Forgetful MCP to be configured in Codex, but it does not ship a static `.mcp.json`. Forgetful can be stdio, local HTTP, remote HTTP, authenticated HTTP, or a custom command, so `$forgetful-install` walks the user through the right setup.

Standard local setup:

```bash
codex mcp add forgetful -- uvx forgetful-ai
```

For HTTP:

```bash
codex mcp add forgetful --url http://localhost:8020/mcp
```

Context7 is optional but recommended for framework-specific documentation.
