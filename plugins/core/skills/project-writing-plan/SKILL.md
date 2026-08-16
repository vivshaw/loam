---
name: project-writing-plan
description: Use when a design spec is complete and the project needs a task breakdown for engineers with zero codebase context.
user-invocable: false
---

# Writing a Project Plan

## Overview

Write comprehensive project plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to verify it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the `core:project-writing-plan` skill to create the project plan."

**Save plans to:** `.loam/tasks/YYYY-MM-DD-<feature-name>/phase_##.md`

## Design Specs Provide Direction, Not Code

Design specs state requirements and a general approach, not implementation. Generate code fresh from codebase investigation instead of copying from the spec. A spec may be weeks old, and the codebase has moved since — investigation reveals the patterns, dependencies, and constraints that actually exist. If a spec does contain code, it is a contract shape, not a suggested implementation.

The spec tells you what must be true when you're done. Investigation tells you how to get there from where you are.

## Before Starting

Verify scope and codebase state.

### 1. Derive the Phase Breakdown

The design spec states requirements, not phases. You must derive the build order. This depends on the codebase as it actually is, which a spec written weeks ago can't know.

Read the spec's `## Requirements` and `## Approach`, then group the requirements into sequential phases:

- Each phase achieves one cohesive goal and ends with a working build
- Every requirement lands in exactly one phase — the phase that *completes* it
- Dependencies run forward only: a phase never needs something a later phase builds
- Infrastructure and scaffolding come first, verified operationally rather than by tests
- Target 5-8 phases. Eight is the hard limit; don't pad to reach it

**Use the priorities to fit the budget.** If the requirements won't fit in 8 phases, cut from the bottom — P1-P3 first, then P4-P6 — and say what you cut. Never silently drop a requirement. Never drop a P10 at all. If the ship-blocking requirements alone exceed 8 phases, stop and tell the user:

"The P10 requirements alone need [N] phases, past the 8-phase limit. You can split this into multiple project plans, or cut scope in the spec."

**Present the breakdown before writing anything.** Output each phase with its goal and the requirement IDs it covers:

```
Phase 1: Project scaffolding — infrastructure, no requirements
Phase 2: Token issuance — covers 1.1, 1.2, 3.1
Phase 3: Token validation — covers 2.1, 2.2
Phase 4: Rotation and revocation — covers 1.3, 4.1, 4.2

Deferred: 5.2 (P3), 5.3 (P2) — out of budget at 8 phases.
```

Then AskUserQuestion:
```
Question: "Here's the phase breakdown. Approve, or tell me what to regroup?"
Options:
  - "Approved - proceed"
  - "Needs revision - [describe changes]"
```

Loop until approved. **Every requirement must appear in a phase or in the deferred list.** A requirement in neither is a requirement nobody builds.

If codebase verification (step 3) later contradicts the breakdown — a phase depends on something that doesn't exist, or something is already built — regroup and re-present rather than forcing the tasks to fit.

### 2. Review Mode Selection

**After the phase breakdown is approved, ask how to handle phase reviews:**

Use AskUserQuestion:
```
Question: "How would you like to review the project plan phases?"
Options:
  - "Write all phases to disk, I'll review afterwards"
  - "Review each phase interactively before writing"
```

**Track this choice - it affects the per-phase workflow below.**

### 3. Codebase Verification

Verify current codebase state before writing any task, for every phase. Tasks written against a stale mental model send the executor to files that don't exist. Dispatch `core:researcher-codebase` rather than investigating yourself, and give it the design's assumptions so it can report discrepancies.

Dispatch one `core:researcher-codebase` to understand testing behavior for this project.
- Follow how the codebase tests. Don't prescribe new testing requirements — for example, don't stipulate TDD unless the problem is predominantly functional or a human directs otherwise, and don't assume mocking databases or other external dependencies is acceptable.
- If you find problems that are difficult to test in isolation with mocks, surface the question to the human operator.
- Instruct the subagent to seek out AGENTS.md files that include details on testing behavior, logic, and methodology, and include file references for you to provide in your plan for the executor to pass to its subagents.

Dispatch a second `core:researcher-codebase` simultaneously with:
- "The design assumes these files exist: [list with expected paths/structure from design]"
- "Verify each file exists and report any differences from these assumptions"
- "The design says [feature] is implemented in [location]. Verify this is accurate"
- "Design expects [dependency] version [X]. Check actual version installed"

**Example query to agent:**
```
Design assumptions from .loam/tasks/YYYY-MM-DD-feature/spec.md:
- Auth service in src/services/auth.ts with login() and logout() functions
- User model in src/models/user.ts with email and password fields
- Test file at tests/services/auth.test.ts
- Uses bcrypt dependency for password hashing

Verify these assumptions and report:
1. What exists vs what design expects
2. Any structural differences (different paths, functions, exports)
3. Any missing or additional components
4. Current dependency versions
```

Review investigator findings and note any differences from design assumptions.

The investigator's report removes the need to hedge. Instead of:
- "Update `index.js` if exists"
- "Modify `config.py` (if present)"
- "Create or update `types.ts`"

write what you know:
- "Create `src/auth.ts`" (investigator confirmed doesn't exist)
- "Modify `src/index.ts:45-67`" (investigator confirmed exists, checked line numbers)
- "No changes needed to `config.py`" (investigator confirmed already correct)

**If codebase state differs from design assumptions:** Document the difference and adjust the project plan accordingly.

### 4. External Dependency Research

**When phases involve external libraries or dependencies, research them before writing tasks.**

Use a tiered approach—start with documentation, escalate to source code only when needed.

#### Tier 1: Internet Researcher (default)

Use `core:researcher-internet` for:
- Official documentation and API references
- Common usage patterns and examples
- Standard specifications (OAuth2, JWT, HTTP, etc.)
- Best practices and known gotchas

**This handles ~80% of external dependency questions.** Most integration work follows documented patterns.

#### Tier 2: Remote Code Researcher (escalation)

Use `core:researcher-remote-code` when:
- Documentation doesn't cover your edge case
- You need to understand internal implementation for extension/customization
- Docs describe *what* but you need to know *how*
- Behavior differs from docs and you need ground truth
- You're extending or hooking into library internals

#### Decision Framework

```
Phase involves external dependency?
├─ No → core:researcher-codebase only
└─ Yes → What do we need to know?
    ├─ API usage, standard patterns → core:researcher-internet
    ├─ Standard/spec implementation → core:researcher-internet
    ├─ Implementation internals, extension points → core:researcher-remote-code
    └─ Both local state + external info → core:researcher-combined
```

#### When to Dispatch

**Dispatch `core:researcher-internet` when phase mentions:**
- External packages/libraries to integrate
- Third-party APIs to call
- Standards to implement (OAuth, JWT, OpenAPI, etc.)

**Escalate to `core:researcher-remote-code` when:**
- Internet-researcher returns "docs don't cover this"
- Task requires extending library behavior
- Task requires matching internal patterns not in docs
- You need to understand error handling, edge cases, or internals

#### Reporting Findings

Include external research findings alongside codebase verification:

```markdown
**External dependency investigation findings:**
- ✓ Stripe SDK uses `stripe.customers.create()` with params: {email, name, metadata}
- ✓ OAuth2 refresh flow per RFC 6749 Section 6
- ✗ Design assumed sync API, but library is async-only
- + Error handling uses typed exception hierarchy (StripeError subclasses)
- 📖 Source: [Official docs | RFC spec | Source code @ commit]
```

**Standards vs Implementation:** Standards questions (e.g., "how does OAuth2 work") are core:researcher-internet territory. Implementation questions (e.g., "how does auth0-js store tokens") may require core:researcher-remote-code.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes).**

For functionality tasks:
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

For infrastructure tasks:
- "Create the config file" - step
- "Verify it works (install, build, run)" - step
- "Commit" - step

**Make task dependencies explicit and sequential.** Code that assumes something "will exist somehow" strands the executor.
- Task N requires a helper function? Task N-1 creates it.
- Task N requires bootstrap credentials? A prior task provisions them.

## Task Types: Infrastructure vs Functionality

**Match task structure to what the design phase specifies.**

Classify each phase from your breakdown as infrastructure (verified operationally) or functionality (verified by tests). Your implementation tasks must honor that distinction.

| Phase Type | Task Structure | Verification |
|------------|----------------|--------------|
| Infrastructure | Create files, configure, verify operationally | Commands succeed (install, build, run) |
| Functionality | Write tests, implement, verify tests pass | Tests pass for the behavior |

**Infrastructure tasks** (project setup, config files, dependencies):
- Don't force TDD on scaffolding
- Verification = operational success
- "npm install succeeds" is valid verification
- **Verifies: None** — explicitly state this, don't invent requirements for setup phases

**Functionality tasks** (code that does something):
- Tests are deliverables alongside code
- Each task lists which requirements it verifies (e.g., "Verifies: 1.1, 1.3")
- Tests must verify those specific requirements, not just "test the code"
- Phase ends with passing tests for every requirement listed in the phase's Requirements Coverage

**Test behavior, not implementation.**
- Test that your function produces the right output, not that it called dependencies a certain way
- If you refactored internals but behavior stayed the same, would the test still pass? If no, you're testing implementation details.
- The requirement is the spec: "An expired token shall be rejected with 401" means test the response, not verify that `jwt.verify()` was called

**What doesn't need tests:**
- Types (TypeScript compiler verifies these)
- Dependencies that have their own tests (don't re-test them through your code)
- How you call things (test the result, not the wiring)
- Infrastructure/setup (verify operationally)

**Subcomponent task grouping.** Phases decompose into subcomponents: types → implementation → tests. When writing tasks for a subcomponent, wrap them in subcomponent markers (see "Task and Subcomponent Markers" section):

```markdown
<!-- START_SUBCOMPONENT_A (tasks 1-3) -->
<!-- START_TASK_1 -->
### Task 1: TokenPayload type and TokenConfig
...
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: TokenService implementation
...
<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: TokenService tests
...
<!-- END_TASK_3 -->
<!-- END_SUBCOMPONENT_A -->
```

The execution agent uses these markers to identify related tasks. The tests task proves the subcomponent works.

**Read each requirement's verification clause.** Requirements state how they're checked — "measured at 500 req/s sustained for 10 minutes" is the test spec. Build tasks that produce exactly that check, rather than inventing a different one.

## Plan Document Header

**Start every plan phase document with this header:**

```markdown
# [Feature Name] Project Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Scope:** Phase [N] of [total] (see phase breakdown)

**Codebase verified:** [Date/time of verification]

---

## Requirements Coverage

This phase implements and tests:

### {slug}.1: [Aspect heading from design spec]
- **{slug}.1.1 (P10):** [Copied literally from design spec]
- **{slug}.1.2 (P6):** [Copied literally from design spec]

### {slug}.2: [Aspect heading from design spec]
- **{slug}.2.1 (P10):** [Copied literally from design spec]

---
```

**Requirements Coverage rules:**
- Copy requirement text literally from the design spec — do not paraphrase
- Use the full scoped identifier (e.g., `oauth2-svc-authn.1.1`), not bare `1.1`
- Carry the priority through, so the executor knows what to sacrifice under pressure
- Include only the requirements this phase implements and tests
- Include both the aspect heading (`{slug}.1`) and the specific requirements (`{slug}.1.1`, `{slug}.1.2`)
- Tasks in this phase must produce tests that verify these specific requirements
- A requirement may appear in an earlier phase if partially addressed, but the phase that owns it must complete it

## Task and Subcomponent Markers

**Wrap every task and subcomponent in HTML comment markers** to enable efficient parsing during execution.

### Task Markers

Wrap every task, and give every task heading an unchecked checkbox:

```markdown
<!-- START_TASK_1 -->
- [ ] ### Task 1: [Task Name]
...task content...
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
- [ ] ### Task 2: [Task Name]
...task content...
<!-- END_TASK_2 -->
```

### Subcomponent Markers

When tasks form a logical subcomponent (e.g., types → implementation → tests), wrap the group:

```markdown
<!-- START_SUBCOMPONENT_A (tasks 3-5) -->
<!-- START_TASK_3 -->
- [ ] ### Task 3: TokenService types
...
<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
- [ ] ### Task 4: TokenService implementation
...
<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
- [ ] ### Task 5: TokenService tests
...
<!-- END_TASK_5 -->
<!-- END_SUBCOMPONENT_A -->
```

**Key rules:**
- Tasks are numbered: `START_TASK_1`, `START_TASK_2`, etc.
- Subcomponents use letters: `START_SUBCOMPONENT_A`, `START_SUBCOMPONENT_B`, etc.
- Subcomponent markers name which tasks they contain: `(tasks 3-5)`
- Tasks inside subcomponents still have their own markers
- Standalone tasks (not in a subcomponent) just have task markers

**Why markers:**
- Execution can grep for `START_TASK_` to list all tasks without reading full content
- Execution can extract just the relevant section to pass to core:executor-task
- Reduces context usage during execution (especially with experimental workflow)

## Phase Verification Section

**End every phase file with this section:**

```markdown
---

## Phase Verification

- [ ] Code review passed
```

## Terminal Checklist

**Write `{PLAN_DIR}/final.md` alongside the phase files:**

```markdown
# Final Review Sequence

- [ ] Project context updated
- [ ] Final code review passed
- [ ] Test analysis complete
- [ ] Human test plan written
- [ ] Run summary written for the human operator
```

The summary is the per-phase account described in `core:execute-implement-a-project` §6: tasks implemented, review cycles needed, compromises made, review issues left outstanding.

Its box goes last on purpose. An autonomous run ends the moment nothing is unchecked, so the turn that ticks the final box is the last one anybody sees — the summary has to be written in it.

## Phase-by-Phase Implementation

**Workflow depends on review mode selected above.**

**Step 0: Create granular task tracker with dependencies**

After the phase breakdown is approved, use TaskCreate to create granular sub-tasks for each phase. This structure survives context compaction — which is also why task descriptions carry absolute paths and explicit dependencies.

Before creating tasks, capture absolute paths:
- `DESIGN_PATH`: Absolute path to design spec (e.g., `/Users/ed/project/.loam/tasks/2025-01-24-feature/spec.md`)
- `PLAN_DIR`: Absolute path to project plan directory (e.g., `/Users/ed/project/.loam/tasks/2025-01-24-feature/`)
- `SCRATCHPAD_DIR`: Absolute path to temp directory for subagent scratch files (e.g., `/tmp/plan-2025-01-24-feature-a7f3b2/`)

**Generate a unique session ID for SCRATCHPAD_DIR:**

```bash
SESSION_ID=$(printf '%04x%04x' $RANDOM $RANDOM)
echo "/tmp/plan-$(date +%Y-%m-%d)-${slug}-${SESSION_ID}"
```

The session ID (e.g., `a7f3b2`) ensures isolation between:
- Parallel planning sessions with similar slugs
- Retry attempts (if a plan fails and user starts over)

**SCRATCHPAD_DIR ensures session isolation.** Code reviewers and other subagents should write any temp files here, not to shared locations like `/tmp/`.

**Work from the `## Requirements` section of the design spec.** Requirements are numbered by aspect (1.1, 1.2, 2.1, ...) with a priority, and they define what "done" means. When writing each phase:
1. Take the requirement IDs assigned to this phase in the approved breakdown
2. Copy those requirements literally into the phase's "Requirements Coverage" header section
3. Ensure tasks produce tests that verify each listed requirement

**For each phase N, create these tasks with dependencies:**

```markdown
- [ ] Phase NA: Read requirements for [Phase Name] from {DESIGN_PATH}
      → blocked by: Phase (N-1)D (or nothing if N=1)
- [ ] Phase NB: Investigate codebase for Phase N and activate relevant skills
      → blocked by: Phase NA
- [ ] Phase NC: Research external deps (Phase N)
      → blocked by: Phase NB
- [ ] Phase ND: Write {PLAN_DIR}/phase_0N.md
      → blocked by: Phase NC
```

**Copy task names verbatim.** "Investigate codebase for Phase N and activate relevant skills" needs the "and activate relevant skills" clause — that phrase triggers skill activation after compaction. Paraphrasing drops it.

**After all phase tasks, create finalization task:**

Before creating the Finalization task, check if `.loam/project-plan-guidance.md` exists. If it does, include its absolute path in the task description:

```markdown
# If .loam/project-plan-guidance.md exists:
- [ ] Finalization: Run core:critic-code-reviewer over all phase files (guidance: [absolute path to .loam/project-plan-guidance.md]), fix every issue, minor ones included
      → blocked by: all Phase *D tasks

# If .loam/project-plan-guidance.md does NOT exist:
- [ ] Finalization: Run core:critic-code-reviewer over all phase files, fix every issue, minor ones included
      → blocked by: all Phase *D tasks
```

**Example for a 3-phase breakdown of `/Users/ed/project/.loam/tasks/2025-01-24-oauth/spec.md`:**

```
TaskCreate: "Phase 1A: Read requirements for Token Types from /Users/ed/project/.loam/tasks/2025-01-24-oauth/spec.md"
TaskCreate: "Phase 1B: Investigate codebase for Phase 1 and activate relevant skills"
  → TaskUpdate: addBlockedBy: [1A]
TaskCreate: "Phase 1C: Research external deps (Phase 1)"
  → TaskUpdate: addBlockedBy: [1B]
TaskCreate: "Phase 1D: Write /Users/ed/project/.loam/tasks/2025-01-24-oauth/phase_01.md"
  → TaskUpdate: addBlockedBy: [1C]

TaskCreate: "Phase 2A: Read requirements for Token Service from /Users/ed/project/.loam/tasks/2025-01-24-oauth/spec.md"
  → TaskUpdate: addBlockedBy: [1D]
TaskCreate: "Phase 2B: Investigate codebase for Phase 2 and activate relevant skills"
  → TaskUpdate: addBlockedBy: [2A]
TaskCreate: "Phase 2C: Research external deps (Phase 2)"
  → TaskUpdate: addBlockedBy: [2B]
TaskCreate: "Phase 2D: Write /Users/ed/project/.loam/tasks/2025-01-24-oauth/phase_02.md"
  → TaskUpdate: addBlockedBy: [2C]

TaskCreate: "Phase 3A: Read requirements for Session Manager from /Users/ed/project/.loam/tasks/2025-01-24-oauth/spec.md"
  → TaskUpdate: addBlockedBy: [2D]
TaskCreate: "Phase 3B: Investigate codebase for Phase 3 and activate relevant skills"
  → TaskUpdate: addBlockedBy: [3A]
TaskCreate: "Phase 3C: Research external deps (Phase 3)"
  → TaskUpdate: addBlockedBy: [3B]
TaskCreate: "Phase 3D: Write /Users/ed/project/.loam/tasks/2025-01-24-oauth/phase_03.md"
  → TaskUpdate: addBlockedBy: [3C]

TaskCreate: "Finalization: Run core:critic-code-reviewer over all phase files, fix every issue, minor ones included"
  → TaskUpdate: addBlockedBy: [1D, 2D, 3D]

TaskCreate: "Test Requirements: Generate test-requirements.md from the Requirements section"
  → TaskUpdate: addBlockedBy: [Finalization]
```

**Why absolute paths in task descriptions:** After compaction, the task list is all that remains. Absolute paths ensure you know exactly which files to read/write without relying on context.

**Why dependencies:** Tasks show `[blocked by #X, #Y]` in the task list, making execution order explicit and preventing out-of-order work.

Use TaskUpdate to mark each sub-task as in_progress when starting, completed when done.

---

### If user chose "Review each phase interactively before writing":

**Workflow for each phase (using granular task tracking):**

1. **Task NA: Read the phase's requirements**
   - Mark task NA as in_progress
   - Read the requirements assigned to Phase N in the approved breakdown, from the `## Requirements` section of the design spec
   - Re-read `## Approach` for any decisions this phase depends on
   - Mark task NA as completed

2. **Task NB: Verify codebase state**
   - Mark task NB as in_progress
   - Dispatch core:researcher-codebase with design assumptions for this phase
   - Review investigator findings for discrepancies
   - **Activate relevant skills** based on findings (if not already active):
     - TypeScript code? Activate TypeScript/coding style skills
     - React components? Activate React skills
     - Database work? Activate database skills
     - Match skills to the technologies this phase involves
   - Mark task NB as completed

3. **Task NC: Research external dependencies** (if phase involves them)
   - Mark task NC as in_progress
   - Dispatch core:researcher-internet for docs/standards/API patterns
   - Escalate to core:researcher-remote-code if docs are insufficient
   - Document findings for inclusion in phase output
   - Mark task NC as completed
   - (Skip if no external deps - still mark completed with note "N/A")

4. **Write implementation tasks** for this phase (in memory, not to file):
   - Take the requirement IDs assigned to this phase in the approved breakdown
   - Include the "Requirements Coverage" section with literal requirement copies
   - Write tasks that implement and test each listed requirement

5. **Present to user** - Output the complete phase plan in your message text:

```markdown
**Phase [N]: [Phase Name]**

**Codebase verification findings:**
- ✓ Design assumption confirmed: [what matched]
- ✗ Design assumption incorrect: [what design said] - ACTUALLY: [reality]
- + Found additional: [unexpected things discovered]
- ✓ Dependency confirmed: [library@version]

**External dependency findings:** (if applicable)
- ✓ [Library] API: [what docs/source revealed]
- ✓ Standard: [spec reference and key details]
- ✗ Design assumption incorrect: [what design said] - ACTUALLY: [reality per docs/source]
- 📖 Source: [Official docs | RFC spec | Source code @ commit]

**Implementation tasks based on actual codebase state and external research:**

### Task 1: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**
[Complete code example]

**Step 2: Run test to verify it fails**
[Exact command and expected output]

**Step 3: Write minimal implementation**
[Complete code example]

**Step 4: Run test to verify it passes**
[Exact command and expected output]

**Step 5: Commit**
[Exact git commands]

[Continue for all tasks in this phase...]
```

6. **Use AskUserQuestion:**

**Options:**
- "Approved - proceed to next phase"
- "Needs revision - [describe changes]"
- "Other"

7. **Task ND: Write phase file (if approved)**
   - Mark task ND as in_progress
   - Write to `.loam/tasks/YYYY-MM-DD-<feature-name>/phase_##.md`
   - Plan document contains only the implementation tasks (no verification findings)
   - Mark task ND as completed, continue to next phase

8. **If needs revision:** Revise based on feedback and present again, leaving ND out of in_progress until approved

---

### If user chose "Write all phases to disk, I'll review afterwards":

**Workflow for each phase (using granular task tracking):**

1. **Task NA: Read the phase's requirements**
   - Mark task NA as in_progress
   - Read the requirements assigned to Phase N in the approved breakdown, from the `## Requirements` section of the design spec
   - Re-read `## Approach` for any decisions this phase depends on
   - Mark task NA as completed

2. **Task NB: Verify codebase state**
   - Mark task NB as in_progress
   - Dispatch core:researcher-codebase with design assumptions for this phase
   - Review investigator findings for discrepancies
   - **Activate relevant skills** based on findings (if not already active):
     - TypeScript code? Activate TypeScript/coding style skills
     - React components? Activate React skills
     - Database work? Activate database skills
     - Match skills to the technologies this phase involves
   - Mark task NB as completed

3. **Task NC: Research external dependencies** (if phase involves them)
   - Mark task NC as in_progress
   - Dispatch core:researcher-internet for docs/standards/API patterns
   - Escalate to core:researcher-remote-code if docs are insufficient
   - Mark task NC as completed
   - (Skip if no external deps - still mark completed with note "N/A")

4. **Task ND: Write phase file**
   - Mark task ND as in_progress
   - Take the requirement IDs assigned to this phase in the approved breakdown
   - Include the "Requirements Coverage" section with literal requirement copies from the spec
   - Write implementation tasks that implement and test each listed requirement
   - Write directly to disk at `.loam/tasks/YYYY-MM-DD-<feature-name>/phase_##.md`
   - Mark task ND as completed, continue to next phase

Write phase content straight to disk rather than echoing it to the user.

**After all phases are written:**

Announce: "All [N] phase files written to `.loam/tasks/YYYY-MM-DD-<feature-name>/`. Let me know if any phases need revision."

---

## Task Structure

**Use the appropriate template based on task type (see Task Types section above).**

### Infrastructure Task Template

```markdown
<!-- START_TASK_N -->
- [ ] ### Task N: [Infrastructure Component]

**Files:**
- Create: `package.json`
- Create: `tsconfig.json`

**Step 1: Create the files**

[Complete file contents - no placeholders]

**Step 2: Verify operationally**

Run: `npm install`
Expected: Installs without errors

Run: `npm run build`
Expected: Builds without errors

**Step 3: Commit**

```bash
git add package.json tsconfig.json
git commit -m "chore: initialize project structure"
```
<!-- END_TASK_N -->
```

### Functionality Task Template

```markdown
<!-- START_TASK_N -->
- [ ] ### Task N: [Component Name]

**Verifies:** {slug}.1.1, {slug}.1.3 (list specific requirements this task tests)

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py` (unit|integration|e2e)

**Implementation:**
[Describe what to implement - contracts, behavior, key logic. Include code for complex/non-obvious implementations.]

**Testing:**
Tests must verify each requirement listed above:
- {slug}.1.1: [brief description of what test should verify]
- {slug}.1.3: [brief description of what test should verify]

Follow project testing patterns. Task-implementor generates actual test code at execution time.

**Verification:**
Run: `[test command]`
Expected: All tests pass

**Commit:** `feat: [description]`
<!-- END_TASK_N -->
```

**Key principles for functionality tasks:**

1. **List requirements explicitly.** Every functionality task specifies which requirements it verifies in the "Verifies" field.

2. **Describe tests, don't write test code.** The requirement text is the spec (e.g., "2.1: An expired token shall be rejected with 401"). Task-implementor generates test code at execution time with fresh codebase context.

3. **Include implementation code when non-obvious.** If implementation is complex or project-specific patterns apply, include the code. If it's straightforward given the requirement, describe it.

4. **Specify test type and location.** Unit, integration, or e2e? Which file? This ensures consistency across phases.

**Why no test code in plans:**
- Test code needs actual function signatures from the implementation
- Project testing patterns discovered at execution time
- Requirement text like "An expired token shall be rejected with 401" is already a clear test spec
- Task-implementor has fresher context than project planner

**If you find yourself writing "this won't compile until Phase N+1":** that work belongs in the current phase. _Every phase must be executable with all tests passing when the phase completes._

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "File probably exists, I'll write 'update if exists'" | Investigate with core:researcher-codebase, then write a definitive instruction. |
| "Design spec has code, I'll use that" | The design gives direction. Generate code fresh from investigation. |
| "Phase 3's tests will fail, but Phase 4 fixes them" | Every phase compiles and passes tests before it concludes. |
| "12 phases, but they're small" | The limit is 8. Cut by priority, or let the user rescope — say which you did. |
| "This requirement doesn't fit any phase cleanly" | Then the breakdown is wrong. Regroup rather than dropping it silently. |
| "I'll infer the phases and start writing" | Present the breakdown and get approval. It's the only place the user sees build order before execution. |
| "A comment explains what's needed next" | Code has to run as written. Create a prior task for the dependency. |
| "Infrastructure tasks need TDD too" | Use the infrastructure template and verify operationally. |
| "This requirement has no stated verification" | Surface the gap to the user rather than inventing a check it never asked for. |
| "I'll paraphrase the task name" | Task names are verbatim — "and activate relevant skills" triggers behavior post-compaction. |
| "Relative paths are fine in task descriptions" | Compaction loses surrounding context. Absolute paths keep tasks self-contained. |
| "I know this library from training" | APIs change. core:researcher-internet for docs, core:researcher-remote-code for internals. |
| "This type needs unit tests" | The compiler verifies types. Test behavior, not wiring, and only the requirements. |
| "Test requirements can be generated during execution" | The code reviewer needs them before execution starts. |
| "Minor issues can wait" | Finalization isn't done until zero issues remain. |
| "Validation is overkill for a simple plan" | Simple plans validate quickly. Gaps found now are cheaper than gaps found during execution. |

## When You Don't Know How to Proceed

**If you cannot write executable code without unresolved questions:** stop and ask.

Use AskUserQuestion with:

1. **Exact description of the blocking issue:**
   - What specific implementation decision you cannot make
   - What information is missing from the design
   - What dependencies are undefined

2. **Context about why this blocks you:**
   - Which task/phase this affects
   - What you've already verified via core:researcher-codebase
   - What the design spec says (or doesn't say)

3. **Possible solutions you can see:**
   - Option A: [specific approach with tradeoffs]
   - Option B: [alternative approach with tradeoffs]
   - Option C: [if applicable]

**Example:**
```
I'm blocked on Phase 2, Task 3 (Bootstrap Logto M2M application).

Issue: The code needs Management API credentials to create resources, but those credentials don't exist yet (chicken-egg problem).

Design spec says: "Bootstrap Logto with applications and roles" but doesn't specify how to get initial credentials.

Codebase verification: No existing bootstrap credentials or manual setup documented.

Possible solutions:
A. Add Phase 0: Manual setup - document steps for user to manually create initial M2M app via Logto UI, save credentials to .env
B. Use Logto admin API if available - requires admin credentials in different format
C. Modify Logto docker-compose to inject initial M2M app via environment variables

Which approach should I take?
```

**Never proceed with uncertain implementation. Surface the decision to the user.**

## Requirements Checklist

**Before starting:**
- [ ] Derive the phase breakdown from `## Requirements` + `## Approach`, ≤8 phases
- [ ] Every requirement assigned to a phase or listed as deferred
- [ ] Present the breakdown, get approval via AskUserQuestion
- [ ] Ask user for review mode (batch vs interactive)
- [ ] Capture absolute paths: DESIGN_PATH and PLAN_DIR
- [ ] Create granular task list with TaskCreate (NA, NB, NC, ND per phase + Finalization + Test Requirements)
- [ ] Set up dependencies with TaskUpdate addBlockedBy (see Step 0)
- [ ] Task descriptions include absolute paths (not relative)

**For each phase (tasks NA through ND):**
- [ ] **Task NA:** Mark in_progress, read this phase's requirements from design, mark completed
- [ ] **Task NB:** Mark in_progress, dispatch core:researcher-codebase, review findings, mark completed
- [ ] **Task NC:** Mark in_progress, research external deps if needed (or mark completed with "N/A"), mark completed
- [ ] Write complete tasks with exact paths and code based on investigator and research findings
- [ ] **If interactive mode:** Output complete phase plan, use AskUserQuestion for approval
- [ ] **Task ND:** Mark in_progress, write to absolute path in task description, mark completed

**For each task in the plan:**
- [ ] Task heading carries an unchecked column-0 checkbox: `- [ ] ### Task N: ...`
- [ ] Exact file paths with line numbers for modifications
- [ ] Complete code - zero TODOs, zero unresolved questions in comments
- [ ] Every code example runs immediately without implementation decisions
- [ ] If code references helpers/utilities, prior task creates them
- [ ] Exact commands with expected output
- [ ] No conditional instructions ("if exists", "if needed")

**For each phase file:**
- [ ] Ends with a `## Phase Verification` section containing an unchecked review box

**For the plan directory:**
- [ ] `final.md` written with all five terminal boxes unchecked, run summary last

**Finalization (after all phase ND tasks completed):**
- [ ] Mark Finalization task as in_progress
- [ ] Dispatch core:critic-code-reviewer to validate plan against design
- [ ] Fix every issue, Minor ones included
- [ ] Re-run core:critic-code-reviewer until APPROVED with zero issues
- [ ] Mark Finalization task as completed
- [ ] Proceed to Test Requirements

**Test Requirements (after Finalization):**
- [ ] Mark Test Requirements task as in_progress
- [ ] Dispatch Opus subagent to generate test requirements from the Requirements section
- [ ] **If interactive mode:** Present to user, use AskUserQuestion for approval
- [ ] **If batch mode:** Write directly without asking
- [ ] Write test-requirements.md to PLAN_DIR
- [ ] Mark Test Requirements task as completed
- [ ] Proceed to execution handoff

## Plan Validation (Finalization Task)

**This is a tracked task: "Finalization: Run core:critic-code-reviewer over all phase files, fix every issue, minor ones included"**

After all phase D tasks are completed, mark the Finalization task as in_progress.

### Step 1: Dispatch core:critic-code-reviewer

```
<invoke name="Task">
<parameter name="subagent_type">core:critic-code-reviewer</parameter>
<parameter name="description">Validating project plan against design</parameter>
<parameter name="prompt">
  Review the project plan for completeness and alignment with the design.

  DESIGN_SPEC: [path to design spec, e.g., .loam/tasks/YYYY-MM-DD-feature/spec.md]

  PROJECT_GUIDANCE: [absolute path to .loam/project-plan-guidance.md, or "None" if file does not exist]

  IMPLEMENTATION_PHASES:
  - [path to phase_01.md]
  - [path to phase_02.md]
  - [... all phase files]

  SCRATCHPAD_DIR: [absolute path to session-isolated temp directory, e.g., /tmp/plan-2025-01-24-feature-a7f3b2/]

  If PROJECT_GUIDANCE is not "None", read it first and apply any project-specific
  review criteria, coding standards, or quality gates it specifies in addition to the
  standard review checklist.

  **Session isolation:** Write any scratch files (notes, intermediate analysis, etc.) to
  SCRATCHPAD_DIR, not to shared temp locations. This prevents collisions with parallel sessions.

  Evaluate:
  1. **Coverage**: Does the project plan cover every requirement from the design?
     - Check every numbered requirement in the spec appears in exactly one phase's
       Requirements Coverage section, or was explicitly deferred by priority
     - Check each requirement's stated verification has a corresponding test task
     - Flag any P10 requirement that was deferred

  2. **Gaps**: Are there any missing pieces?
     - Requirements in the spec with no implementation tasks
     - Verification stated in a requirement but missing from implementation tasks
     - Dependencies or setup steps not accounted for

  3. **Alignment**: Does the implementation approach match the design?
     - Decisions from the spec's Approach section followed
     - File paths consistent with codebase verification findings
     - Phase ordering has no forward dependencies

  4. **Executability**: Can each phase be executed independently?
     - Dependencies between tasks are explicit
     - No forward references to code that doesn't exist yet
     - Each phase ends with verifiable state

  Report:
  - GAPS: [list any missing coverage]
  - MISALIGNMENTS: [list any divergence from design]
  - ISSUES: [Critical/Important/Minor issues in the plan itself]
  - ASSESSMENT: APPROVED / NEEDS_REVISION
</parameter>
</invoke>
```

### Step 2: Fix every issue, Minor ones included

Fix every issue, Minor ones included. Finalization isn't complete until the reviewer reports zero.

**If the reviewer returns NEEDS_REVISION or reports any issues:**

1. **Create a task for each issue** (survives compaction):
   ```
   TaskCreate: "Finalization fix [Critical]: <issue description, copied verbatim from the reviewer>"
   TaskCreate: "Finalization fix [Important]: <issue description, copied verbatim from the reviewer>"
   TaskCreate: "Finalization fix [Minor]: <issue description, copied verbatim from the reviewer>"
   ...one task per issue...
   TaskCreate: "Finalization: Re-review after fixes"
   TaskUpdate: set "Re-review" blocked by all fix tasks
   ```

   **Copy issue descriptions verbatim**, even long ones. After compaction the task description is all that remains, so it has to carry the full details.

2. Review the gaps, misalignments, and issues identified
3. Fix all of them — Critical, Important, and Minor
4. Update the relevant phase files
5. Mark each fix task complete as you address it
6. Re-run core:critic-code-reviewer validation
7. If more issues found, create new individual fix tasks and repeat
8. Mark "Re-review" complete when zero issues

A minor issue deferred to execution is a minor issue the executor hits without the planning context that would let it judge the tradeoff. Fix them here.

### Step 3: Complete finalization

**Only when core:critic-code-reviewer returns APPROVED with zero issues:**

Mark the Finalization task as completed.

Proceed to Test Requirements generation.

## Test Requirements Generation

**Tracked task: "Test Requirements: Generate test-requirements.md from the Requirements section"**

Mark in_progress after Finalization completes.

Test requirements map each requirement to specific automated tests, and identify requirements needing human verification. The core:critic-test-analyst agent uses this during execution to validate coverage.

**Step 1: Generate via subagent**

```
<invoke name="Task">
<parameter name="subagent_type">core:general-purpose-opus</parameter>
<parameter name="description">Generating test requirements from the Requirements section</parameter>
<parameter name="prompt">
Read the design at [DESIGN_PATH] and implementation phases in [PLAN_DIR].

The design spec's `## Requirements` section is numbered by aspect (1.1, 1.2, 2.1, …), each
requirement carrying a priority from P1 to P10. Many requirements state their own verification
("measured at 500 req/s sustained for 10 minutes") — use that as the test spec rather than
inventing a different check.

Generate test-requirements.md mapping each requirement, by its scoped ID, to:
- Automated tests: requirement, test type (unit/integration/e2e), expected test file path
- Human verification: requirements that can't be automated, with justification and approach

Rationalize against implementation decisions made during planning. Every requirement must map
to either an automated test or documented human verification. Note any that were deferred
during phase derivation, with their priority.
</parameter>
</invoke>
```

**Step 2: Handle based on review mode**

- **Interactive mode:** Present to user, AskUserQuestion for approval. This is the LAST interactive item.
- **Batch mode:** Write directly, announce completion.

**If user requests revisions in interactive mode:**

1. **Create a task for each revision** (survives compaction):
   ```
   TaskCreate: "Test requirements fix: <revision request, copied verbatim from the user>"
   ...one task per revision...
   TaskCreate: "Test requirements: Re-present for approval"
   TaskUpdate: set "Re-present" blocked by all fix tasks
   ```

   **Copy revision requests verbatim**, even long ones — after compaction, the task description is all that remains.

2. Address each revision, marking tasks complete as you go
3. Re-present for approval
4. Repeat until approved

**Step 3: Write and complete**

Write to `[PLAN_DIR]/test-requirements.md`. Mark task completed. Proceed to execution handoff.

## Execution Handoff

After Test Requirements generation completes, announce:

**"Project plan complete and validated. Saved to [count] phase files + test-requirements.md in `.loam/tasks/YYYY-MM-DD-<feature-name>/`. The first phase file is `<full-path>`. Test requirements are in `<full-path>/test-requirements.md`."**

