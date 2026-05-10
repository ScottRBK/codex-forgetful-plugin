---
name: forgetful-project-init
description: Initialize Forgetful project context for the current Codex session by matching the current working directory to a Forgetful project, loading recent project memories, and asking before creating a missing project.
---

# Forgetful Project Init

Use this skill when a session starts in a repository or when the user wants to initialize Forgetful project context.

Keep this workflow quiet. Do the checks, then report only the useful result.

## Workflow

1. Determine the current working directory from session context.
2. Discover project candidates:

```text
execute_forgetful_tool("list_projects", {})
```

3. Match the current directory to a Forgetful project. Prefer repository metadata from the git remote when available, then project name or project notes. Do not guess a project ID.
4. If a project matches, load recent project memories:

```text
execute_forgetful_tool("get_recent_memories", {
  "limit": 10,
  "project_ids": [PROJECT_ID]
})
```

Briefly mention the matched project and the relevant memory context found. If there are no memories, say that directly.

5. If no project matches, ask the user whether they want to create a Forgetful project for this directory. Do not create it without confirmation.
6. When a project exists or the user confirms creation, maintain a device/location note:
   - Discover the current device from runtime context, such as hostname or environment details available in the session.
   - Search for an existing device entity before creating one.
   - Link the device entity to the project.
   - Create or update one project-scoped memory noting this project's local path on that device.

## Project Creation

If the user confirms project creation, use:

```text
execute_forgetful_tool("create_project", {
  "name": "<project name>",
  "description": "<short purpose/scope>",
  "project_type": "development",
  "repo_name": "<owner/repo when known>"
})
```

Choose a conservative project type from the available Forgetful schema. Use `development` unless the project is clearly documentation, infrastructure, personal, open-source, or another supported type.

## Privacy And Distribution

This skill is distributed publicly. Do not hardcode or assume private names, hostnames, local paths, repository owners, or user-specific conventions. Use only runtime-discovered values and user-confirmed information.

Do not save secrets or credentials in project, entity, or memory notes.
