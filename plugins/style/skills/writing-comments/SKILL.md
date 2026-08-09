---
name: writing-comments
description: Use every time you write or edit code comments, or perform code review
---

# Writing excellent comments

Follow this guide to write proper code comments. Excellent comments can make code simple to understand. Poor comments can add visual noise, bury other engineers in irrelevant information, and rapidly become outdated over time.

Comments are excellent for:

- Explaining _why_ the code is implemented a particular way.
- Giving context that cannot be conveyed through naming.
- Documenting non-obvious constraints.

## **Don't** leave comments that restate the code

Legible, self-evident code is superior to ambiguous code with an accompanying explanation.
A comment restating the obvious purpose of adjacent code is noise. Comments should only be present where the code cannot speak for itself.

### Information Litmus Test

Imagine an engineer is reading this section of code for the first time. Does this comment tell them anything they would not know from reading the code alone?

If the comment only narrates what the code already says, it does not belong in the file.

### Examples

**Wrong.** Each of these only restates the code beneath it:

```
// Load the network policy from the config
const policy = loadOptions(config).policy

// Skip sending metrics for users with disabled telemetry
if (user.enableTelemetry) {
  sendMetric()
}
```

**Correct.** Each of these carries something the code cannot.

```
// The upstream returns 409 for a short window after a write, before the
// record becomes readable. This is not a real conflict.
if (res.status === 409) return retry(req)

// First match wins, so the catch-all has to stay last.
rules := []Rule{denyInternal, allowVetted, allowAll}

// This encoded value ships in a cookie, so it must stay under 4 KiB.
state := encodeState(session)
```

### Red flags

A comment _may_ be restating the code if it:

- Names the function called on the line below it
- Restates the condition of the `if` it precedes
- Opens with a verb mirroring the call beneath — *Load*, *Get*, *Set*, *Create*, *Check*, *Loop over*
- Conveys a fact a reader could recover in seconds

### Rationalizations

| Excuse | Reality |
|--------|---------|
| "More comments make the code more approachable" | Check the Information Litmus Test. A comment that repeats the code adds no value. |
| "This helps a less experienced reader" | A reader who cannot follow the code will not be rescued by a paraphrase of it. |
| "This code is confusing, so it needs a comment" | Confusing code needs to be fixed. Comment only what is still non-obvious afterward. |
| "It's one line, it costs nothing" | It costs a second copy of the logic that nothing keeps in sync. It will outlive its accuracy. |

## **Don't** leave archaeological comments

**This section is especially critical.** Write comments for a future reader of the file, in its end state. Not for the reviewer of this change. The reviewer has the diff. Not for your current user. The user has the session log. The file outlives these, and everyone who reads it afterward has only the end state.

### Reader Litmus Test

Imagine a newly-joined engineer who has never seen the code you just changed is reading your file. Does the comment tell them anything actionable — an invariant, a constraint, a warning, a task?

If it only makes sense next to the old code — arguing the change is safe, narrating what moved — it does not belong in the file.

#### Do not delete a comment merely because it mentions the past

Some comments reference the past legitimately and should stay:

- `@deprecated` and backcompat markers — forward guidance for future callers
- TODOs that use the prior state to describe the intended next step
- App history or real-world history: `// deprecated in Docker 18.09, kept for back-compatibility`. This describes the world, not this diff.

### Examples

#### Temporal narration

Don't describe the change, describe only the end state.

```
// Wrong. Narrates the change.
// Proxy is a host-enforced network policy, which replaced the tinyproxy
// allowlist proxy from the prior version.

// Correct. States what is true.
// Proxy is a host-enforced network policy.
```

#### Change rationale in place of design explanation

Don't describe why the design beats what came before, describe only what the design is.

```
// Wrong. Measures against an unstated baseline — the old code.
// Using a single container provides better parallelism than one container per sandbox.

// Correct. Conveys the design as it stands.
// One container serves every sandbox concurrently.
```

#### Comparatives that launder history into the present tense

A comment does not have to say "no longer" to be about the diff. A contrast describes history whenever the thing being negated exists only in the repo's past, the session log, or a prior project plan.

```
// Wrong. Nothing named SessionStore exists in this tree. The reader is
// handed a question they can only answer from an old project plan.
// Auth tokens live on the request context, not in a SessionStore.

// Correct. The fact, plus the constraint that makes it worth stating.
// Auth tokens live on the request context and do not outlive the request.
// Do not stash them on a long-lived struct.
```

**Test:** would a reader who has never seen this repo assume the thing you are negating? If not, delete the contrast — you are describing a ghost.

#### Outdated test contracts

Test comments deserve special attention. State only the contract the test verifies now.

```
// Wrong. Justifies the new assertion by contrast with the old.
// now returns 3 args instead of 2, since we added the proxy flag

// Correct. States the current contract.
// dry-run emits the proxy flag even when no policy is configured
```

### Red flags

A comment _may_ be archaeological if it:

- Contains *now*, *no longer*, *instead of*, *previously*, *used to*
- Contains `not X`, `rather than X`, `as opposed to X`, where X is not a live alternative
- Uses a comparative — *better*, *simpler*, *faster* — with no stated baseline; the implied baseline is the old code
- Names a component you cannot grep for in the current tree
- Argues that a change is safe or correct
- Makes sense only if you know what the code looked like before

### Rationalizations

| Excuse | Reality |
|--------|---------|
| "The contrast explains why this design won" | The reader never saw the loser. State what is true, not what it beat. |
| "It's present tense, so it's current state" | Present tense can hide history. Ask whether the negated thing exists in the current code. |
| "Reviewers need to know this is safe" | Reviewers have the diff. The file outlives the review. |
| "It mentions the past, so it has to go" | Check the Reader Litmus Test. Deprecation markers, TODOs, and real-world history stay. |

## Sum-up

### When authoring

1. **Start with good names and structure.** Reach for a clearer name, type, or extracted function before reaching for a comment.
2. **Comment what isn't obvious.** If the code is clear, but there are reasons, context, or constraints it doesn't convey, write a comment to convey them.
3. **Cut narration.** Check the Information Litmus Test and Reader Litmus Test. If your comment can be derived from the line below it, delete the comment. If your comment describes irrelevant past states, delete the comment.

### When reviewing

1. **Cut narration, don't reword it.** A better-phrased restatement is still a restatement.
2. **Fix the code, not the comment.** A comment propping up a confusing name or shape means rename or restructure, then drop the comment.
3. **Leave load-bearing comments alone.** Why, context, and constraints stay.
4. **Double-check AI output.** AI agents have a tendency to create low-value comments. Be doubly vigilant when reviewing AI-generated code.
