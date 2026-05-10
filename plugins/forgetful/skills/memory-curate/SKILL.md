---
name: memory-curate
description: Curate durable knowledge from the completed Codex turn into Forgetful memory. Use when asked to save or curate memory, or when the conversation produced reusable decisions, preferences, project knowledge, or technical patterns worth preserving.
---

# Memory Curate

Use this skill to decide whether the completed turn contains durable knowledge that should be saved to Forgetful, then perform careful curation.

This skill is deliberately stricter than ordinary note-taking. Most turns should not create memories.

## Trigger

When asked to curate memory, inspect the completed turn and decide whether there is reusable knowledge. If nothing qualifies, reply exactly:

```text
Forgetful memory curation: No durable memory to save.
```

## What Qualifies

Create or update memories for:

- Important decisions with rationale.
- Technical patterns Scottesh wants reused.
- Project-specific gotchas, conventions, or architecture that will matter later.
- Strong user preferences or workflows.
- Durable plugin behavior or setup decisions.

Do not save:

- Routine progress updates.
- Temporary file paths unless they are part of durable project structure.
- Raw command output.
- Obvious facts from common documentation.
- Low-confidence summaries.
- Anything below importance 7.

## Workflow

1. Identify at most three candidate memories from the completed turn.
2. Discard candidates that are not reusable, durable, and important.
3. For each remaining candidate, query Forgetful before writing:

```text
execute_forgetful_tool("query_memory", {
  "query": "<candidate topic>",
  "query_context": "Checking for existing memories before automatic curation",
  "k": 5,
  "include_links": true
})
```

4. Choose the safest action:

| Situation | Action |
|-----------|--------|
| Existing memory is accurate but incomplete | `update_memory` |
| Existing memory is contradicted by explicit new decision | create replacement, then `mark_memory_obsolete` with `superseded_by` |
| Existing memory is related and still accurate | create memory if truly distinct, then `link_memories` |
| Existing memory already covers the candidate | do nothing |
| No related memory exists | create a new atomic memory |

5. Prefer one high-quality memory over several weak memories.
6. Report what happened in a short final note.

## Atomic Memory Rules

Each saved memory must:

- Represent one concept, fact, decision, or pattern.
- Have a short searchable title.
- Fit within 2000 characters.
- Include why it matters in `context`.
- Use no more than 10 keywords and 10 tags.
- Use importance 7-10 only.

## Project Association

When project association is obvious from the current repository or prior memory context, use `project_ids`. If uncertain, omit project association rather than guessing.

Do not assume project ID 1.

## Reporting

If a memory is created with importance >= 7, announce:

```text
Forgetful memory curation:
Saved to memory: "<title>"
Tags: [tags]
Related: [linked memory titles or "none"]
```

If existing memory was updated or obsoleted, include the memory title or ID and the action taken.

If nothing qualifies, reply exactly:

```text
Forgetful memory curation: No durable memory to save.
```
