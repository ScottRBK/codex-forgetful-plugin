---
name: context-gather
description: Gather implementation context before planning or coding by delegating retrieval to subagents that combine Forgetful memory, local code inspection, Context7 documentation, and web search when needed. Use when Scottesh asks to gather context, run context_gather, prepare an implementation brief, or check prior decisions and framework guidance before making changes.
---

# Context Gather

Use this skill to produce a focused implementation briefing before planning or changing code.

The point of this workflow is context isolation: retrieval is noisy, tool-heavy work, so the main agent should delegate it and receive only the synthesized result.

## Workflow

1. Restate the task in one sentence.
2. Launch a subagent for retrieval. Treat an explicit request for `context_gather`, `forgetful:context_gather`, `context-gather`, "gather context", or an implementation brief as permission to delegate this retrieval work.
3. Instruct the subagent to query Forgetful memory first, across all projects unless Scottesh explicitly asks for a project scope.
4. Instruct the subagent to follow relevant memory links:
   - Read linked memories when they clarify decisions or evolution.
   - Fetch linked code artifacts and documents when they may contain reusable implementation details.
5. Instruct the subagent to inspect dependency manifests and imports before recommending new code paths.
6. In parallel, the main agent may inspect a small number of obvious local files only when needed to frame the task or validate the final brief. Do not duplicate the subagent's broad retrieval work.
7. Have the subagent query Context7 for framework or library guidance when the task names a library, framework, or API.
8. Have the subagent use web search only when memory, local files, and Context7 do not provide enough current or authoritative context.
9. Wait for the subagent's brief before planning or implementing.
10. Return the synthesized brief, then wait for Scottesh or continue only if the original request also asked for implementation.

## Subagent Contract

Use a subagent by default for this skill. The subagent absorbs the context cost of memory searches, linked artifact reads, documentation lookup, and broad file exploration.

Prompt the subagent with a bounded read-only task:

```text
Gather context for this task: <task>

Use Forgetful memory across all projects first. Follow relevant linked memories, code artifacts, and documents. Inspect local code where memory references files or where existing patterns matter. Check dependency manifests and imports before recommending new implementations. Use Context7 for task-specific framework/library docs. Use web search only as a fallback for current authoritative information.

Return only a synthesized implementation brief with:
- Relevant memory and decisions
- Current code patterns and files
- Framework guidance
- Implementation constraints, risks, and test implications

Do not edit files.
```

Prefer one retrieval subagent. Use multiple subagents only when the task naturally splits into independent areas, such as separate backend/frontend/framework questions.

## Forgetful Usage

The retrieval subagent should use the available Forgetful MCP server in the current session. Normal calls should go through `execute_forgetful_tool`.

Start broad:

```text
execute_forgetful_tool("query_memory", {
  "query": "<task essence and likely technologies>",
  "query_context": "Gathering context before planning or implementation",
  "k": 8,
  "include_links": true,
  "max_links_per_primary": 5
})
```

Do not apply `project_ids` initially unless the user explicitly scoped the task. Cross-project recall is the point of this workflow.

Useful follow-up tools:

- `get_memory` for linked memories that look relevant.
- `get_code_artifact` for linked reusable snippets or reference implementations.
- `get_document` for linked design notes, ADRs, or long-form explanations.
- `search_entities`, `get_entity_memories`, and relationship tools when an org, service, device, or person is central to the task.

## Local Code Inspection

The retrieval subagent should use `rg` and targeted file reads before drawing conclusions about the current repo. Prefer actual code over memory when they disagree.

Look for:

- Existing patterns and helper APIs.
- Tests covering the relevant behavior.
- Configuration, dependency, and integration points.
- Dependency manifests and import statements.
- Places where memory references may be stale.

## Context7

When the task names a library or framework, the retrieval subagent should use Context7:

1. Resolve the library ID.
2. Query specific documentation for the task topic.
3. Include only guidance that affects implementation choices.

Do not query generic docs just to fill space.

## Output Format

The subagent should return this shape to the main agent:

```markdown
# Context for: <task>

## Relevant Memory

- <memory title or ID>: <decision, pattern, or gotcha and why it matters>

## Current Code

- <file/path>: <what exists now and how it affects the task>

## Framework Guidance

- <library>: <specific Context7 guidance, if used>

## Implementation Notes

- <constraints, risks, likely approach, test implications>
```

Keep the brief focused. Include code snippets only when they are directly reusable or needed to explain the pattern.

## Avoid

- Dumping unsynthesized memory results.
- Listing memory IDs without reading relevant linked artifacts.
- Treating memories as newer than code without checking.
- Searching the web before checking Forgetful, local files, and Context7.
- Creating memories during the gather pass unless Scottesh explicitly asks or the session produces a reusable new decision.
