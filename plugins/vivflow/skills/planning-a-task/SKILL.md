---
name: planning-a-task
description: "Use when /vivflow:plan is invoked, to translate a goal into a self-contained spec at .vivflow/tasks/<slug>/plan.md. Orchestrates pinning down the goal, grounding in codebase reality, resolving open questions, designing the approach with trade-offs, deriving testable acceptance criteria, mapping files, decomposing into TDD-sized tasks, and handoff to the writing-plans shape-guide. Plans carry no question marks."
user-invocable: false
---

# Planning a task

Plan a piece of work — translate a goal into something a reader could act on without further conversation.

This is active engineering, not transcription. You are figuring out what "done" actually means, learning what the codebase looks like *today* (not what you remember), picking an approach with the trade-offs named out loud, and breaking the work into steps that can be executed one at a time without surprise. The file produced (`plan.md` in `.vivflow/tasks/<slug>/`) is a means; the thinking that produces it is the work.

Write for a reader who is competent at engineering but has **no context** for this codebase, this problem, or the decisions that shaped the plan. If something isn't in the plan, it isn't known. That bar is what makes a plan a self-contained artifact instead of notes-to-self — and it forces you to make implicit decisions explicit before you stop thinking about them.

A good plan does six things:

1. Pins down what the goal actually means.
2. Surfaces what the codebase looks like *now*, not what you remember.
3. Picks an approach with the trade-offs named out loud.
4. Derives acceptance criteria that are objectively testable.
5. Decomposes work into TDD-sized tasks ordered by risk.
6. Leaves no question marks for the reader.

The steps below walk through that work. They scale with the size of the change — a one-line fix doesn't need a half-hour of codebase verification — but they don't get skipped. Skipping is what produces plans a reader can't act on without second-guessing.

## 1. Pick the task folder

In priority order:

- If the user named an existing task slug in the invocation, use `.vivflow/tasks/<slug>/`.
- If `/vivflow:research` ran earlier in this conversation, use that slug from context.
- Otherwise, derive a new slug from the goal (`YYYY-MM-DD-<kebab-name>`, today's date) and create `.vivflow/tasks/<slug>/`.

## 2. Pin down the goal

Restate the goal in your own words. If you can only restate it by paraphrasing the user's phrasing, you don't yet understand it.

Surface ambiguity *now*, when it's cheap to resolve. Ask the user whichever of these are genuinely unclear:

- What does success look like — what would you point at and say "done"?
- What's explicitly *not* the goal? (Boundaries are often easier to ask about than scope.)
- Who is this for? Audience usually constrains design.
- Are there constraints I should know about — deadline, deps, perf budget, compatibility?

Don't run the whole list as ceremony. Ask what's actually unclear; skip what's already known. The point is to flush ambiguity to the surface before it ossifies into invented constraints in the plan.

## 3. Read research, if any

If `research.md` exists in the task folder, read it in full. Note any **open questions** flagged for the user — those block the plan.

If `research.md` doesn't exist, that's fine — research is optional for planning. But for anything more than a trivial change, step 4 will end up doing the work research would have done, just inline.

## 4. Ground in codebase reality

Plans built on remembered or assumed codebase state turn into implementations that don't compile or quietly duplicate things that already exist. Before designing an approach, gather the actual state of the area the work will land in:

- **Read the files**, not just grep them. Grep tells you a name exists; reading tells you what it actually does.
- **Run the existing tests once** to see the baseline pass/fail state. If anything's already broken, your change shouldn't be blamed for it later.
- **Check `git log -20 -- <path>`** for the area. Recent activity tells you what's in flux. Old quiet code tells you the conventions are settled.
- **Grep for the symbols you'll touch** — find every call site, every type user, every test reference. These are the surfaces your change will perturb.
- **Skim adjacent files** to learn the local conventions: naming, file layout, test patterns, error handling, logging idioms. Plans that fight conventions lose.

The amount of grounding scales with the change. A one-line bug fix needs less than a feature that crosses three modules. When in doubt, read more — uncovered assumptions are expensive at implementation time.

If research already covered this thoroughly, confirm it's still current and move on.

## 5. External research, if needed

For unfamiliar libraries, frameworks, protocols, or patterns:

- Read the official docs for the version actually installed (check `package.json` / `Cargo.toml` / equivalent first).
- Check the changelog for breaking changes between the version you're reading about and the version actually in use.
- If you're choosing between options, look at similar implementations in other open source projects — a real working example beats a marketing comparison every time.
- For protocols / RFCs / specs, read the actual spec, not a summary post.

Don't over-research. If you can already plan well without it, skip it. External research costs context window and time; spend both deliberately.

## 6. Resolve open questions

Every open question from research, from step 2, or from steps 4-5 gets resolved before the plan is written.

- Questions about user intent, preferences, scope, or taste: **ask the user**.
- Questions you can answer yourself by reading code, running a command, or searching the web: **answer them yourself**, then move on.
- Don't paper over an unknown with "TBD" or "we'll figure this out" — the reader will treat it as decided, and decide wrong.

The finished plan carries no question marks. Plans are where questions get answered, not where they live.

## 7. Escape hatch

If after steps 1-6 the work is genuinely a one-line config tweak, a typo fix, or a single trivial utility, say so and offer to skip planning entirely. Trust the user to know when ceremony is overkill.

Otherwise, proceed.

## 8. Design the approach

Generate 2-4 candidate approaches. For each, write a one-paragraph description, the key trade-off, and what it makes easier vs harder. Two is the minimum — without alternatives, you don't actually have a choice, you have an assumption.

Pick one. The rationale should answer *why this trade-off, here*. Not "this seems good" — say what you're optimizing for and what you're accepting in return.

Note what would change the choice. "If we later need X, we'd switch to approach B" — this gives the reader (and future-you) the early-warning signal for when the design starts to strain.

Approach is design, not code. "Use Postgres advisory locks for serialization, accepting that lock contention scales with shard count" is enough. Don't pre-write the SQL — that's implementation, and writing it now binds the reader to choices made without seeing the surrounding code.

## 9. Derive acceptance criteria

Translate the goal into a bulleted list of objectively verifiable checks. Each criterion is something an LLM with no context could test pass/fail in under a minute.

Then run two coverage checks:

- **Goal coverage** — if every criterion passes, is the goal accomplished? Gaps mean missing criteria.
- **Anti-coverage** — are there behaviors the implementation should *not* exhibit? List explicit anti-criteria for regressions you want to avoid. (E.g., "no existing public API signatures change.")

If a criterion can't be made testable, the goal underneath it is still fuzzy — go back to step 2.

## 10. Map the files

List every file you'll add or edit, one line each with a few words on what changes. Also list files you'll **read but not modify** — those constrain the design and should be visible to the reader.

Cross-check the file map against the task breakdown (next step):

- Every file in the map should be touched by at least one task.
- Every task should touch files in the map.

Mismatches mean one of the two is wrong.

Before adding a file in a new directory, grep the repo for similar files to confirm the convention. The codebase has opinions about layout. Inventing a new directory structure is a planning smell — and a sign you haven't grounded deeply enough in step 4.

## 11. Decompose into tasks

Each task is one TDD cycle: red → green → refactor. Right size is about 5-30 minutes of work depending on language and surface area.

Order by **risk, not by ease**. The hardest unknown gets tackled first — if it's going to fail, fail it cheaply, before you've built out scaffolding around it. Don't put a deceptively easy task first to feel productive; ease-first ordering produces nice early progress and late catastrophic surprises.

Each task should leave the codebase in a working state — tests green, build clean. "This won't compile until task 5 lands" means the task is the wrong size; split it so each step is independently shippable in principle.

Mark dependencies explicitly:

- Default is sequential.
- Parallel groups need to be called out (`tasks 4-6 can run in parallel after task 3`).
- Forward references ("depends on task 8" when you're writing task 2) usually mean the order is wrong; reorder.

For each task, include: the change in one sentence, the file(s) it touches, the test cases that will drive it, and any sequencing notes.

## 12. Surface risks and unknowns

Before locking the plan, ask yourself four questions:

- What's the riskiest assumption in the approach? Does a task validate it early?
- Where are the integration points — places where this change meets the rest of the system? Each is a place for surprise.
- What's the fallback if the chosen approach fails halfway through? Could the work be paused without leaving the codebase broken?
- What's the smallest version of this that would prove the design works? (If it's much smaller than the full plan, consider building it first as a prototype task.)

If any of these surface real concerns, fold them into the plan — usually as an early validation task, an explicit out-of-scope deferral, or a noted fallback.

## 13. Define out of scope

For each item you're deferring, write two things: the **temptation** (what made you want to include it) and the **reason for deferring** (a condition, a future signal, a decision that needs to be made first).

- Weak: "perf out of scope."
- Useful: "Perf optimization deferred until baseline metrics show the hot path is actually the bottleneck. Premature optimization here would couple the design to assumptions we haven't validated."

A good out-of-scope entry lets a future reader see why something was *not* done, so they can revisit when conditions change. A weak one is just a label that means "we ran out of time to think about this."

## 14. Validate before writing

Walk this checklist. Anything that fails goes back to the relevant step before you write the plan:

- [ ] Goal is restated in plain English and the user has confirmed it (or it's so clearly stated in the invocation that confirmation is redundant).
- [ ] Every acceptance criterion is testable in under a minute by someone with no context.
- [ ] The set of criteria covers the goal — no gap where the goal could be unmet despite all criteria passing.
- [ ] The approach has named alternatives that were considered and rejected.
- [ ] The file map and the task breakdown cross-check both ways.
- [ ] The first task tackles the riskiest unknown, not the easiest thing.
- [ ] Each task individually leaves the codebase buildable and tested.
- [ ] No "TBD," "we'll figure out," "details to follow," or other deferred decisions appear anywhere.
- [ ] No "we will" / "should" / "could" preamble — the plan says what gets built, not what someone intends to build.

## 15. Write the plan

Use the `writing-plans` skill — it shapes the artifact (sections, headings, voice, per-section quality heuristics). Write to `.vivflow/tasks/<slug>/plan.md`.

**Verify, don't assume.** Every element of the plan traces to direct user input, research findings, or something you observed in steps 4-5. If you can't trace it, don't add it.

## 16. Report

Print the slug and the path. One line.

---

## Common planning anti-patterns

These show up across the steps above. Watch for them and treat them as signals to back up:

- **Vague criteria** — "auth works," "handles errors gracefully." Not testable. Back to step 9.
- **Forward references** — "we'll handle X when Y is done." Pull X into the plan, or explicitly out-of-scope it with a reason.
- **Phantom dependencies** — planning around a library that doesn't actually solve your problem. Read its docs in step 5; confirm.
- **Hand-waving** — "TBD," "we'll figure this out," "details to follow." Resolve in step 6 or remove.
- **Scope creep** — adding features the user didn't ask for. Move to out-of-scope with the temptation named, or ask the user.
- **Premature abstraction** — a generic solution for a specific need. Build the specific thing first; the right abstraction emerges from the second or third use case, not the first.
- **First-step bias** — ordering tasks by ease so progress feels fast. Order by risk instead.
- **Plan-driven code** — writing implementation details into the plan ("here's the SQL," "here's the Python"). Approach is design; code belongs to the implementation phase, not the planning one.
- **Phantom users** — designing for hypothetical future users the actual user didn't mention. Build for the real one; the future user can ask later.

## When to stop and ask the user

You're about to make a call the user should make. Ask, don't decide, when:

- The goal itself is ambiguous, or two readings of it produce materially different plans.
- Two approaches have different user-visible implications (UI changes, perf trade-offs, API surface changes, behavior changes the user will notice).
- Verifying an assumption requires access you don't have (credentials, environment, third-party system, internal business context).
- The scope feels much larger than the user described — they may not have realized.
- A constraint the user mentioned conflicts with one you discovered in step 4 — the resolution is a design call, not a research call.

The cost of asking is one round-trip. The cost of building the wrong thing is the whole implementation.
