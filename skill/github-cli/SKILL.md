---
name: github-cli
description: "Interact with GitHub using the gh CLI - PRs, issues, repos, releases, and actions. Trigger terms: github, gh, pull request, PR, issue, release, actions, workflow, repo."
---

## Use when
- Creating, viewing, or merging pull requests
- Managing issues (create, close, comment)
- Checking workflow/action status
- Creating releases
- Cloning or forking repos

## Don't use when
- Local git operations (use `git` directly)
- Non-GitHub remotes (GitLab, Bitbucket)

## Outputs
- PRs, issues, releases, or action logs in GitHub (no local files unless explicitly created).

## Templates or Examples
- Use the command tables below as templates.

## Prerequisites
- `gh` CLI installed
- SSH key configured for GitHub access

## Quick Reference

### Pull Requests
| Action | Command |
|--------|---------|
| List PRs | `gh pr list` |
| View PR | `gh pr view <number>` |
| Create PR | `gh pr create --title "..." --body "..."` |
| Checkout PR | `gh pr checkout <number>` |
| Merge PR | `gh pr merge <number>` |
| PR diff | `gh pr diff <number>` |
| PR checks | `gh pr checks <number>` |

### Issues
| Action | Command |
|--------|---------|
| List issues | `gh issue list` |
| View issue | `gh issue view <number>` |
| Create issue | `gh issue create --title "..." --body "..."` |
| Close issue | `gh issue close <number>` |
| Comment | `gh issue comment <number> --body "..."` |

### Repos & Releases
| Action | Command |
|--------|---------|
| Clone | `gh repo clone <owner>/<repo>` |
| Fork | `gh repo fork <owner>/<repo>` |
| View repo | `gh repo view` |
| Create release | `gh release create <tag> --title "..." --notes "..."` |
| List releases | `gh release list` |

### Actions & Workflows
| Action | Command |
|--------|---------|
| List runs | `gh run list` |
| View run | `gh run view <run-id>` |
| Watch run | `gh run watch <run-id>` |
| Rerun failed | `gh run rerun <run-id> --failed` |
| List workflows | `gh workflow list` |

### API & GraphQL

**REST API:**
```bash
gh api repos/<owner>/<repo>/pulls
gh api repos/<owner>/<repo>/issues/<number>/comments
```

**GraphQL** (for data not exposed by `gh pr view`):
```bash
# List PR review threads (gh pr view doesn't expose these)
gh api graphql -F owner=<owner> -F name=<repo> -F number=<pr> -f query='
query($owner:String!, $name:String!, $number:Int!){
  repository(owner:$owner,name:$name){
    pullRequest(number:$number){
      reviewThreads(first:100){
        nodes{id isResolved isOutdated comments(first:50){nodes{id author{login} body}}}
        pageInfo{hasNextPage endCursor}
      }
    }
  }
}'

# Resolve a review thread
gh api graphql -F threadId=<threadId> -f query='
mutation($threadId:ID!){
  resolveReviewThread(input:{threadId:$threadId}){thread{isResolved}}
}'
```

**Pagination:** If `pageInfo.hasNextPage` is true, repeat with `after: "<endCursor>"`.

## Procedure

1. Ensure `gh auth status` shows authenticated
2. Use `gh pr list` or `gh issue list` to find items
3. Perform action with appropriate command
4. Verify with `gh pr checks` or `gh run list`
5. Always use a heredoc with --body-file or a specific encoding that supports \n correctly

## Checks & Guardrails
- Always check PR status before merging
- Use `--draft` for work-in-progress PRs
- Prefer `gh pr merge --squash` for clean history
- Check `gh run list` after pushing to verify CI
- Use GraphQL for review threads (`gh pr view` doesn't expose them)
- Handle pagination when results exceed 100 items
