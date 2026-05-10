---
name: forgetful-project-load
description: Load recent Forgetful context for an already registered project by matching the current working directory to a Forgetful project and retrieving recent project-scoped memories. Use when the user asks to load, refresh, resume, or catch up on recent Forgetful project information.
---

# Forgetful Project Load

Use this skill when the user wants recent Forgetful context for the current repository.

This skill is read-only. Do not create projects, memories, entities, or links. If no matching project exists, report that and suggest `$forgetful-project-init`.

## Workflow

1. Determine the current working directory from session context.
2. Discover project candidates:

```text
execute_forgetful_tool("list_projects", {})
```

3. Match the current directory to a Forgetful project. Prefer repository metadata from the git remote when available, then project name or project notes. Do not guess a project ID.
4. If no project matches, say that no existing Forgetful project matched the directory and stop.
5. Load recent project memories:

```text
execute_forgetful_tool("get_recent_memories", {
  "limit": 10,
  "project_ids": [PROJECT_ID]
})
```

6. If the user gave a task or topic, also run a focused semantic query:

```text
execute_forgetful_tool("query_memory", {
  "query": "<task or topic>",
  "query_context": "Loading project-scoped Forgetful context for the current Codex session",
  "project_ids": [PROJECT_ID]
})
```

7. Briefly report:
   - matched project name and ID
   - number of recent memories found
   - the highest-signal decisions, patterns, or gotchas relevant to the current task

If there are no project memories, say that directly.

## Privacy And Distribution

This skill is distributed publicly. Do not hardcode or assume private names, hostnames, local paths, repository owners, or user-specific conventions. Use only runtime-discovered values and user-confirmed information.

Do not surface secrets or credentials if they appear in retrieved context.
