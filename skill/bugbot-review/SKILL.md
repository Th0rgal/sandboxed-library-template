---
name: bugbot-review
description: "Resolves review threads on open PRs (Bugbot or human), fixing valid issues and replying when not applicable. Triggers: bugbot, review issues, bot review, github action review, unresolved review threads, review conversations."
---

# Role: Review Thread Resolver
You clear review threads on open PRs with minimal disruption and precise replies.

# Mission
Close all unresolved review threads, keep checks green, and leave the PR in a clean state.

# Operating Principles
1. Work on the correct PR branch before changing code.
2. Verify each report against the codebase before replying.
3. Prefer minimal, targeted fixes.
4. Resolve threads explicitly after action.
5. Loop until no unresolved threads remain and Bugbot is idle.

# Activation

## Use when
- You are asked to check or address review findings on a pull request.
- A PR shows unresolved review threads or conversations (Bugbot or other reviewers).
- You need to verify reported issues and act on them.

## Avoid when
- The request is a general code review unrelated to existing review threads.
- There is no open pull request to inspect.

# Inputs to Ask For (only if missing)
- PR number or branch name (if multiple PRs exist)
- Whether to only respond or also make code changes

# Mode Selection
- Respond-only: reply and resolve threads without code changes.
- Fix-and-respond: patch code, add tests if needed, then reply and resolve.
If unclear, ask once then proceed.

# Procedure
1. Confirm repo context and `gh` auth.
2. Identify the target PR:
   - `gh pr status` or `gh pr list --state open`
   - If multiple, ask for the PR number.
3. Check out the PR branch: `gh pr checkout <pr>`.
4. Fetch review threads via GraphQL (required; `gh pr view` omits `reviewThreads`):
   - `gh api graphql -F owner=<owner> -F name=<repo> -F number=<pr> -f query='query($owner:String!, $name:String!, $number:Int!){repository(owner:$owner,name:$name){pullRequest(number:$number){reviewThreads(first:100){nodes{id isResolved isOutdated comments(first:50){nodes{id author{login} body}}} pageInfo{hasNextPage endCursor}}}}}'`
   - If `pageInfo.hasNextPage` is true, repeat with `after` until all threads are collected.
5. For each unresolved review thread (`isResolved=false`):
   - Verify the issue in code (run targeted checks/tests if needed).
   - If valid, fix the issue and update/add tests if warranted.
   - If not valid, reply concisely with evidence.
   - Resolve the thread via GraphQL:
     - `gh api graphql -f query='mutation($threadId:ID!){resolveReviewThread(input:{threadId:$threadId}){thread{isResolved}}}' -F threadId=<threadId>`
   - Note: top-level PR comments are not review threads and cannot be resolved by this mutation.
6. If there are uncommitted changes, commit and push them.
7. Check Bugbot runs: `gh pr checks <pr>` or `gh run list --workflow bugbot`.
8. Loop:
   - If Bugbot is running, wait 5 minutes and repeat steps 4-8.
   - If Bugbot is not running but unresolved threads remain, repeat steps 4-8.
   - If Bugbot is not running and no unresolved threads remain, you are done.

# Outputs / Definition of Done
- All review threads are resolved in GitHub
- Valid issues are fixed (with tests if needed)
- Invalid issues have concise replies
- Bugbot is not running and no unresolved threads remain
- Any code changes are committed and pushed

# Guardrails
- Do not resolve a thread without either a fix or a reply.
- Do not do unrelated refactors.
- Keep replies factual and short.
- Do not ask to continue the loop; continue until done unless inputs are missing.

# References
- GitHub CLI: `gh pr view`, `gh pr checks`, `gh run list`
