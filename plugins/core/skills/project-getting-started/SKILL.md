---
name: project-getting-started
description: Use when starting a project from a design spec.
user-invocable: false
---

# Getting Started on a Project

## Overview

Orchestrate the transition from design spec to executable implementation through planning and execution handoff.

**Core principle:** Branch -> Plan -> Execute. Isolate work, create detailed tasks, hand off to execution.

**Announce at start:** "I'm using the `core:project-getting-started` skill to create the project plan from your design."

## Design Spec Path

If the user hasn't provided a path to a design spec, ask for it rather than guessing.

Use AskUserQuestion:
```
Question: "Which design spec should I create a project plan for?"
Options:
  - [list any design specs you find in .loam/tasks/]
  - "Let me provide the path"
```

If `.loam/tasks/` doesn't exist or is empty, ask the user to provide the path directly.

**Never assume, infer, or guess which design spec to use.** The user must explicitly tell you.

## The Process

This skill has three steps:

1. **Branch Setup:** Select and create branch for implementation
2. **Planning:** Create detailed project plan
3. **Execution Handoff:** Direct user to execute the plan

**Step 0: Create orchestration task tracker**

Use TaskCreate to track the orchestration steps:

```
TaskCreate: "Branch setup"
(conditional) TaskCreate: "Read project implementation guidance from [absolute path]"
  → TaskUpdate: addBlockedBy: [Branch setup]
  → (only if .loam/project-plan-guidance.md exists)
TaskCreate: "Create project plan"
  → TaskUpdate: addBlockedBy: [Branch setup] (or [Read guidance] if it exists)
TaskCreate: "Re-read `core:project-getting-started` skill (restore context)"
  → (leave blockedBy unset for now — it gets updated once the granular tasks exist)
TaskCreate: "Execution handoff"
  → TaskUpdate: addBlockedBy: [Re-read skill]
```

Re-point the "Re-read skill" task once `core:project-writing-plan` has created the Finalization task. See "After Planning: Update Dependencies" below.

The "Create project plan" task wraps the granular tasks created by `core:project-writing-plan`. The "Re-read skill" step ensures context is restored after potential compaction before handoff.

### Branch Setup

Mark "Branch setup" task as in_progress.

Before planning, set up the branch and workspace for implementation work.

Extract the **slug** from the design spec filename (everything after `YYYY-MM-DD-`, excluding `.md`). For example, `oauth2-svc-authn` from `2025-01-18-oauth2-svc-authn.md`.

This slug is used for:
1. Project plan directory name (`.loam/tasks/YYYY-MM-DD-{slug}/`)
2. **Scoping all AC identifiers** — every acceptance criterion uses the format `{slug}.AC{N}.{M}`

The slug ensures AC identifiers are globally unique across multiple plan-and-execute rounds.

**Set up branch:**

1. Ask user which branch to use:
   ```
   Question: "Which branch should I use for this implementation?"
   Options:
     - "Use current branch" (stay on current branch, no branch creation)
     - "[friendly-name]" (e.g., oauth2-svc-authn)
     - "$(whoami)/[friendly-name]" (e.g., ed/oauth2-svc-authn)
   ```
2. **If "Use current branch":** Continue with current branch (no git commands)
3. **If branch name provided:**
   - Determine main branch name: Check if `main` or `master` exists
   - Create new branch from main/master: `git checkout -b [branch-name] origin/[main-or-master]`
   - Verify branch created successfully
   - Announce: "Created and checked out branch `[branch-name]` from `origin/[main-or-master]`"
4. **If branch creation fails:** Report error to user and ask if they want to use current branch instead

Mark "Branch setup" task as completed. **THEN proceed to Planning.**

### Check for Implementation Guidance

After branch setup, check for project-specific implementation guidance.

**Check if `.loam/project-plan-guidance.md` exists:**

Use the Read tool to check if `.loam/project-plan-guidance.md` exists in the session's working directory.

**If the file exists:**

1. Use TaskCreate to add: "Read project implementation guidance from [absolute path to .loam/project-plan-guidance.md]"
   - Set this task as blocked by "Branch setup"
   - Update "Create project plan" to be blocked by this new task
2. Mark the task in_progress
3. Read the file and incorporate the guidance into your understanding
4. Mark the task completed
5. Proceed to Planning

**If the file does not exist:**

Proceed directly to Planning. Do not create a task or mention the missing file.

**What implementation guidance provides:**
- Coding standards and conventions
- Testing requirements and patterns
- Review criteria beyond defaults
- Project-specific quality gates

### Planning

Mark "Create project plan" task as in_progress.

Use `core:project-writing-plan`.

Announce: "I'm using the `core:project-writing-plan` skill to create the detailed project plan."

The `core:project-writing-plan` skill will:
- Verify scope (<=8 phases from design spec)
- Verify codebase state with investigator
- Create phase-by-phase implementation tasks
- Validate each phase with user before proceeding
- Write project plan to `.loam/tasks/`

**Output:** Complete project plan written to files, on appropriate branch.

Mark "Create project plan" task as completed.

### After Planning: Update Dependencies

Update the "Re-read skill" task to be blocked by Finalization.

The granular tasks are now created. Find the Finalization task ID and update dependencies:

```
TaskUpdate: "Re-read `core:project-getting-started` skill"
  → addBlockedBy: [Finalization task ID]
```

This ensures the task list shows the correct order:
```
✔ #1 Branch setup
✔ #2 Create project plan
✔ #5 Phase 1A: Read [Phase Name] from /path/to/design.md
✔ #6 Phase 1B: Investigate codebase for Phase 1
...
✔ #N Finalization: Run core:critic-code-reviewer...
◻ #3 Re-read skill › blocked by #N
◻ #4 Execution handoff › blocked by #3
```

### Restore Context (Before Handoff)

Mark "Re-read `core:project-getting-started` skill (restore context)" task as in_progress.

Re-read this skill before proceeding to handoff.

After potentially long planning work (especially if context compaction occurred), re-read this skill file to ensure you have accurate instructions for the execution handoff:

```bash
# Re-read this skill to restore context
cat /path/to/plugins/core/skills/project-getting-started/SKILL.md
```

Or use the Read tool on the skill file path.

**Why this matters:** After compaction, you may have lost details about the handoff process. Re-reading ensures you provide correct absolute paths and instructions.

Mark "Re-read `core:project-getting-started` skill" task as completed.

### Execution Handoff

Mark "Execution handoff" task as in_progress.

After planning is complete, hand off to execution.

Don't invoke execute-plan directly — the user needs to /clear context first.

**Step 1: Capture and verify absolute paths**

Before outputting the handoff instructions, run these commands to get real, verified paths:

```bash
# Get absolute path to current working tree root
git rev-parse --show-toplevel
```

Capture this output as `WORKING_ROOT`.

Then construct and verify the project plan path exists:

```bash
# Verify project plan directory exists
# Replace YYYY-MM-DD-feature-name with the actual plan directory name
ls -d "${WORKING_ROOT}/.loam/tasks/YYYY-MM-DD-feature-name"
```

**Both commands must succeed.** If the plan directory doesn't exist, something went wrong during planning — investigate before proceeding.

**Step 2: Provide copy-paste instructions with verified absolute paths**

Use the actual paths you captured and verified in Step 1. Example output:

```
Project plan complete!

Ready to execute? This requires fresh context to work effectively.

**Copy the instruction below before running /clear — it erases this conversation.**

(1) Copy this now:

Use the core:execute-implement-a-project skill for /Users/ed/project/.loam/tasks/2025-01-17-oauth2-feature/

(2) Clear your context:

/clear

(3) Paste and run the copied command.

That skill will implement the plan task-by-task with code review between tasks.
```

**Use the real paths from Step 1, not placeholders.** The example above shows the format — substitute your actual verified paths.

**Why absolute paths:** After /clear, Claude Code returns to the original session directory, which may not be where the plan lives. Absolute paths ensure execution happens in the correct directory regardless of where /clear returns.

**Why /clear instead of continuing:**
- Execution needs fresh context to work effectively
- Long conversations accumulate context that degrades quality
- /clear gives the execution phase a clean slate

Mark "Execution handoff" task as completed.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Invoking core:execute-implement-a-project directly | Provide copy-paste instructions instead |
| Not warning user to copy the instruction before /clear | Always warn: "Copy this before running /clear" |
| Using relative paths in the handoff instruction | Run bash commands to get absolute paths, verify they exist |
| Outputting placeholder paths like `[WORKING_ROOT]` | Output real paths from `git rev-parse --show-toplevel` and `ls -d` |
| Not verifying plan directory exists | Always `ls -d` the full plan path before outputting command |
| Passing phase_01.md instead of directory | Pass the directory so all phases execute |
| Forgetting to mention /clear | Always tell user to /clear before execute |
| Skipping "Re-read skill" step before handoff | Always re-read this skill to restore context post-compaction |
| Not creating orchestration tasks at start | Create Branch setup, Planning, Re-read, Handoff tasks in Step 0 |
| Not re-pointing "Re-read skill" after planning | Must update addBlockedBy to Finalization task, not "Create project plan" |

## Integration with Workflow

This skill sits between design and execution:

```
Design Spec (in .loam/tasks/)
  -> User invokes core:project-getting-started with the design spec path

Getting Started on a Project (this skill)
  -> Step 0: Create orchestration tasks
    -> [ ] Branch setup
    -> [ ] Create project plan
    -> [ ] Re-read skill (restore context)
    -> [ ] Execution handoff

  -> Branch Setup [tracked task]
    -> Ask which branch, create if needed

  -> Planning [tracked task wrapping granular tasks]
    -> Invoke `core:project-writing-plan`
    -> Creates granular tasks per phase (NA, NB, NC, ND)
    -> Creates Finalization task (code review, fix every issue)
    -> Write to .loam/tasks/

  -> After Planning: Update Dependencies
    -> Re-point "Re-read skill" to be blocked by Finalization task
    -> Ensures correct execution order in task list

  -> Restore Context [tracked task, blocked by Finalization]
    -> Re-read this skill file
    -> Ensures handoff instructions are accurate post-compaction

  -> Execution Handoff [tracked task]
    -> Run `git rev-parse --show-toplevel` for absolute paths
    -> Verify plan directory exists
    -> Output command with verified absolute paths
    -> Provide /clear command

Execute Project Plan (next step)
  -> Reads project plan
  -> Implements task-by-task
  -> Code review between tasks
```

**Purpose:** Bridge design and execution with appropriate branch isolation, granular task tracking that survives compaction, and context restoration.
