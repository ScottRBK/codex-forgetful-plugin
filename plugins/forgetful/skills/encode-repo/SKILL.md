---
name: encode-repo
description: Bootstrap a repository into Forgetful by creating or updating the project, memories, entities, relationships, documents, and code artifacts. Use when Scottesh asks to encode a repo, bootstrap a codebase into memory, port the Claude /encode-repo workflow, or prepare a project for future agent context retrieval.
---

# Encode Repo

Use this skill to systematically populate Forgetful with durable repository knowledge.

This is the Codex skill form of Scottesh's Claude Code `/encode-repo` command. It uses local code inspection plus Forgetful MCP meta-tools. It does not require Serena; if symbol-level LSP analysis is explicitly requested, gather context first and confirm the available tooling before extending this workflow.

## Inputs

Parse the user request for:

- Repository path: default to the current working directory.
- Project name: optional override; otherwise infer from git remote, directory name, or package metadata.
- Phase scope: optional subset; otherwise run all phases in order.

Before writing memories, state the detected path, project name, and phase scope.

## Required Forgetful Flow

Use `execute_forgetful_tool` for normal work.

Start with:

```text
execute_forgetful_tool("list_projects", {})
```

Then query existing coverage:

```text
execute_forgetful_tool("query_memory", {
  "query": "<project-name> architecture overview technology stack testing patterns",
  "query_context": "Assessing existing knowledge base coverage before repository encoding",
  "k": 10,
  "include_links": true,
  "project_ids": [<project_id if known>]
})
```

If the project exists, reuse its `project_id`. If it does not exist, create it in Phase 1.

## Phase Gates

Do not proceed past a mandatory phase until its minimum is met, unless the user explicitly narrows the phase scope.

After each phase, report:

```text
Phase <N> Complete:
- Created/updated: <counts by type>
- Minimum required: <target>
- Status: Met / Not met / Skipped with reason
```

Mandatory phases:

- Phase 0: discovery and gap analysis.
- Phase 1: project foundation, including project record and 5 core memories.
- Phase 2: architecture memories, one per major layer.
- Phase 2B: entity graph, minimum 3 entities.
- Phase 3: implementation patterns, minimum 3 memories.
- Phase 6: code artifacts, minimum 3 artifacts.

Conditional phases:

- Phase 4: features, only when distinct features exist.
- Phase 5: decisions, only when explicit decision documentation exists.
- Phase 7: documents, only when long-form reference content is useful.

## Phase 0: Discovery

Inspect the repository before creating anything.

Use `rg --files`, manifest reads, README/docs reads, and targeted `rg` searches. Prefer structured manifests over inference when available.

Assess:

- Size: small `<5K LOC`, medium `5K-50K LOC`, large `>50K LOC`.
- File count: small `<50`, medium `50-500`, large `>500`.
- Type: app, library, CLI, service, integration, monorepo, docs, or mixed.
- Existing KB coverage and likely stale memories.
- Key entry points, test commands, configuration, and dependency manifests.

Report a concise gap analysis before proceeding.

## Phase 1: Foundation

Create the project if missing:

```text
execute_forgetful_tool("create_project", {
  "name": "owner/repo-name or directory-name",
  "description": "<problem solved, main features, tech stack>",
  "project_type": "development",
  "repo_name": "<owner/repo when known>",
  "notes": "<run/test/configuration primer>"
})
```

If the project exists but `notes` are stale or empty, update them with a short primer:

- Entry points and commands.
- Tech stack.
- Architecture summary.
- Key patterns.
- Top components.

Create or update these five memories with `project_ids`:

- Project overview, importance 10.
- Technology stack, importance 9.
- Architecture pattern, importance 10.
- Development setup, importance 8.
- Testing strategy, importance 8.

Query for likely duplicates before creating. Prefer updating stale memories over creating near-duplicates.

## Phase 2: Architecture

Create one atomic architecture memory per major layer or subsystem.

Common layers:

- Routes, controllers, CLI commands, or user-facing entry points.
- Service or business logic.
- Repository, persistence, or data access.
- Models, schemas, domain entities, or types.
- Middleware, auth, configuration, jobs, integrations, UI state, or build tooling.

Memory shape:

```text
title: "<Project> - <Layer> Layer"
content: "Purpose, location, main files, interactions, and implementation patterns."
context: "Understanding this layer for future changes."
tags: ["architecture", "layer"]
importance: 8
project_ids: [<project_id>]
```

## Phase 2B: Entity Graph

Create at least 3 entities for any encoded project. Check for duplicates first:

```text
execute_forgetful_tool("search_entities", {
  "query": "<entity-name>",
  "limit": 5
})
```

Create entities for major components, external services, frameworks, databases, and key abstractions. Use `entity_type: "other"` with a practical `custom_type` such as `Component`, `Service`, `Library`, `Framework`, `Database`, `Tool`, or `Pattern`.

Then create relationships where useful:

- `uses`
- `depends_on`
- `calls`
- `extends`
- `implements`
- `connects_to`
- `contains`

Link important entities back to relevant memories with `link_entity_to_memory`.

## Phase 3: Patterns

Document at least 3 recurring implementation patterns.

Search for:

- Dependency injection and construction patterns.
- Error handling.
- Database/session/transaction patterns.
- Async/concurrency.
- Validation/schema handling.
- Caching.
- Event, queue, or webhook handling.
- Configuration and secrets.
- Testing fixtures and mocks.

Pattern memories should include where the pattern lives, how it is used, and example files without pasting large code blocks.

## Phase 4: Features

Run only when the repository has distinct user-facing, integration, background, or business features.

For each major feature, create 1-2 memories covering:

- User or system outcome.
- Entry point.
- Flow through components.
- Key dependencies and configuration.
- Important tests.

Skip with a clear message when the project is a single-purpose library or has no distinct feature boundaries.

## Phase 5: Documented Decisions

This phase is documentation-only. Never infer decisions from observed code.

Create decision memories only from:

- ADRs or decision docs.
- README sections titled `Why`, `Rationale`, or `Design Decisions`.
- Comments explicitly stating a choice and reason.
- CONTRIBUTING, DESIGN, or architecture docs with rationale.

Do not create decision memories for plain technology choices, framework conventions, or your assumptions.

Include the source path in the memory content.

## Phase 6: Code Artifacts

Create at least 3 code artifacts for reusable implementation examples.

Good artifact categories:

- Configuration loading.
- Database/session setup.
- Route, handler, or command pattern.
- Error handling.
- Authentication/authorization flow.
- Testing fixture or mock pattern.
- Logging/observability setup.
- Background task or worker pattern.

Use actual code excerpts that are long enough to be useful and short enough to remain reusable. Link related memories by updating their `code_artifact_ids` when appropriate.

## Phase 7: Documents

Create documents only for long-form content that should not be forced into atomic memories:

- Architecture reference.
- API reference.
- Deployment guide.
- Symbol or component index.
- Operational runbook.

For every document, create or update 1-3 atomic entry-point memories linked with `document_ids`.

## Final Validation

Run validation queries scoped to the project:

```text
execute_forgetful_tool("query_memory", {
  "query": "How is this codebase architected?",
  "query_context": "Validating repository encoding coverage",
  "project_ids": [<project_id>]
})
```

Also query for testing/setup and a major feature or component.

Finish with:

- Project ID and name.
- Counts for memories, entities, relationships, artifacts, and documents.
- Phase status table.
- Validation query results summary.
- Any gaps intentionally left for later.

## Quality Rules

- One concept per memory.
- Prefer 200-400 words per memory.
- Use source paths and concrete file names.
- Use honest importance scores; most memories should be 7-8.
- Update stale memories instead of duplicating them.
- Mark obsolete memories that reference removed code.
- Avoid secrets, credentials, generated files, and vendor code.
