# Addressing GitHub PR feedback

When asked to review and address the feedback on a pull request:

**Requires:** `gh` CLI (authenticated), `TaskCreate` tool

## 1. Gather the context
- Fetch the PR details.
- Fetch the detailed comments.
- Read all relevant files to understand context.

## 2. Evaluate feedback and prioritize response
- Categorize each comment by severity: `Critical` > `Important` > `Good Suggestion` > `Low Priority`.
- Check if issues are already fixed before proposing changes.
- Identify any false positives.

## 3. Process each comment (in priority order)
For each comment:

**A) Present the original comment:** Show the full text so the user can see what's being addressed.
**B) Provide your evaluation:** Is it valid? Already fixed? False positive?
**C) Propose the fix:** Show the exact edit you'll make (if any), then wait for the user's approval.
**D) After the user approves:**
  1. Make the code/spec edit.
  2. Draft the GitHub reply. **SKIP PLEASANTRIES** like "nice catch", etc. Be professional but not so laudatory.
  3. Show the proposed reply to the user, but **do not** post it.

## 4. Handle Volume
If there are many comments and you are concerned about context space:
- Create Claude tasks (`TaskCreate`) for each comment with: title, comment ID, file, summary, suggested fix.
- Use task descriptions to capture priority context (critical, important, good suggestion, low priority).
- If the PR comment was already tracked as a task, don't forget to mark it completed.
