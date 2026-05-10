# Context Hub for Codex

Context Hub packages Scottesh's context-gather workflow for Codex.

The plugin focuses on one workflow: gather implementation context before planning or coding. It adapts the Claude Code `/context_gather` pattern into a Codex skill plus command shims.

## What It Does

- Delegates retrieval to a subagent so noisy memory, documentation, and code search do not flood the main agent context.
- Searches Forgetful memory across all projects by default.
- Follows linked memories, documents, code artifacts, and skills when they clarify the task.
- Inspects local code with targeted `rg` and file reads.
- Uses Context7 for library and framework guidance when relevant.
- Uses web search only as a fallback for current authoritative context.

## Commands

- `/context_gather <task>`: gather a focused implementation brief before planning or editing.
- `/context-hub-install`: check and configure Codex dependencies for Forgetful and Context7.

## Install From A Cloned Repo

From a clone of this repository:

```bash
codex plugin marketplace add /path/to/context-hub-plugin
```

Then open Codex with the plugin enabled and run:

```text
/context-hub-install
```

## Dependencies

Context Hub expects Forgetful MCP to be configured in Codex. Standard local setup:

```bash
codex mcp add forgetful -- uvx forgetful-ai
```

For HTTP:

```bash
codex mcp add forgetful --url http://localhost:8020/mcp
```

Context7 is optional but recommended for framework-specific documentation.
