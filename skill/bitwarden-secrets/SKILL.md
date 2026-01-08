---
name: bitwarden-secrets
description: >
  Retrieve and manage secrets using Bitwarden Secrets Manager CLI (bws).
  Trigger terms: bitwarden, secrets, bws, secret, api key, credentials, password.
---

## When to Use
- Retrieving API keys, passwords, or credentials for a task
- Listing available secrets or projects
- Creating or updating secrets

## When NOT to Use
- Storing secrets in code or config files (use bws instead)
- Managing Bitwarden vault items (use `bw` CLI, not `bws`)

## Prerequisites
- `bws` CLI installed
- `BWS_ACCESS_TOKEN` environment variable set

## Quick Reference

| Action | Command |
|--------|---------|
| Get secret | `bws secret get <SECRET_ID>` |
| List secrets | `bws secret list` |
| List in project | `bws secret list <PROJECT_ID>` |
| List projects | `bws project list` |
| Create secret | `bws secret create <KEY> <VALUE> <PROJECT_ID>` |
| Edit secret | `bws secret edit <SECRET_ID> --value <VALUE>` |
| Delete secret | `bws secret delete <SECRET_ID>` |

## Output Formats
Use `--output` flag: `json`, `yaml`, `table`, `tsv`, `env`

```bash
bws secret get <ID> --output json
bws secret list --output table
```

## Procedure

1. **List projects** to find where secrets are stored
2. **List secrets** in the relevant project
3. **Get secret** by ID to retrieve the value
4. Use the secret value in your task (don't log it)

## Checks & Guardrails
- Never echo or log secret values
- Don't commit secrets to git
- Use `--output json` for parsing in scripts
