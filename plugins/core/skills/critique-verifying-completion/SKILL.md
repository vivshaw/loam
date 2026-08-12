---
name: critique-verifying-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
user-invocable: false
---

# Verification Before Completion

## Overview

**Core principle:** evidence before claims. An unverified "it works" reads exactly like a verified one, so the person downstream can't tell which they got — that's what makes it costly.

If you haven't run the verification command, you can't claim it passes.

## The Gate Function

```
Before claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the full command, fresh
3. READ: Full output, check exit code, count failures
4. VERIFY: Does the output confirm the claim?
   - If no: state the actual status, with evidence
   - If yes: state the claim, with evidence
5. Only then: make the claim
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- Any wording implying success without having run verification

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification. |
| "I'm confident" | Confidence isn't evidence. |
| "Linter passed" | The linter isn't the compiler. |
| "Agent said success" | Verify independently. |
| "Partial check is enough" | A partial check proves the part you checked. |
| "Different words, so the rule doesn't apply" | The rule is about the implication, not the phrasing. |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (should fail) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## When To Apply

Before:
- Any claim of success or completion, however phrased
- Any expression of satisfaction, or positive statement about the state of the work
- Committing, PR creation, task completion
- Moving to the next task
- Delegating to agents

Phrasing doesn't matter — paraphrases, synonyms, and mere implications of success all count.

Run the command. Read the output. Then claim the result.
