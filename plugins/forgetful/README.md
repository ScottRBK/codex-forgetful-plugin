# Forgetful for Codex

Forgetful packages Scottesh's context-gather workflow for Codex.

The plugin focuses on two Codex skills:

- `$context-gather`: gather implementation context before planning or coding.
- `$forgetful-install`: configure Forgetful MCP and optional Context7 MCP for the local Codex environment.

## What It Does

- Delegates retrieval to a subagent so noisy memory, documentation, and code search do not flood the main agent context.
- Searches Forgetful memory across all projects by default.
- Follows linked memories, documents, code artifacts, and skills when they clarify the task.
- Inspects local code with targeted `rg` and file reads.
- Uses Context7 for library and framework guidance when relevant.
- Uses web search only as a fallback for current authoritative context.

## Skills

- `$context-gather <task>`: gather a focused implementation brief before planning or editing.
- `$forgetful-install`: check and configure Codex dependencies for Forgetful and Context7.

## Install From A Cloned Repo

From a clone of this repository:

```bash
codex plugin marketplace add /path/to/codex-forgetful-plugin
```

Then restart Codex, open `/plugins`, install and enable `Forgetful`, start a new thread, and run:

```text
$forgetful-install
```

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
