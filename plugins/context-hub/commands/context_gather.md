---
description: Gather focused context from Forgetful memory, local code, Context7 docs, and web fallback before planning or implementation
argument-hint: [task-description]
---

# Context Gather

Use the `$context-gather` skill for the following task:

$ARGUMENTS

## Instructions

1. Treat this command as explicit permission to delegate retrieval to a subagent.
2. Have the retrieval subagent search Forgetful memory across all projects first.
3. Have the subagent follow relevant linked memories, documents, code artifacts, files, and skills.
4. Have the subagent inspect local code patterns with targeted searches and file reads.
5. Have the subagent query Context7 when the task names a library, framework, or API.
6. Use web search only when memory, local code, and Context7 do not provide enough current or authoritative context.
7. Wait for the implementation brief before planning or editing.

Return the brief in the shape defined by the `context-gather` skill.
