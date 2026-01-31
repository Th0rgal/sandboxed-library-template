---
name: bitwarden-secrets
description: >
  Manage and retrieve secrets from Bitwarden Secrets Manager using the bws CLI
  for user simulation and automated testing purposes.
  Trigger terms: bitwarden, bws, secrets manager, credentials, api keys, secrets,
  machine account, access token, inject secrets, environment variables, user simulation,
  test credentials, login credentials.
---

## When to Use
- **User simulation testing**: Retrieving login credentials for agent-browser to simulate real user flows
- Retrieving secrets from Bitwarden Secrets Manager for a project
- Setting up a new project with Bitwarden Secrets Manager
- Injecting secrets into application runtime via `bws run`
- Syncing Bitwarden secrets to local `.env` files (encrypted with dotenvx)
- Managing secrets across multiple projects/environments
- Automated E2E testing that requires real user credentials

## When NOT to Use
- The user wants you (the agent) to handle actual secret values directly
- Simple local-only secrets that don't need centralized management
- One-time passwords or TOTP codes (use Bitwarden Password Manager)

## Primary Use Case: User Simulation with Browser Automation

This skill is designed to work alongside browser automation tools to enable realistic user simulation. The workflow is:

1. **Retrieve credentials** from Bitwarden Secrets Manager (email, password, API keys)
2. **Use browser automation** to interact with those credentials
3. **Simulate real user flows** (login, form submission, authenticated actions)

### Browser Automation Tool

Use **agent-browser** CLI for all browser automation. Do NOT use Playwright MCP tools.

| Environment | Tool | Notes |
|-------------|------|-------|
| **All environments** | agent-browser | Use `agent-browser <command>` CLI |
| **Cloud/Serverless** | Cloud-native browser | Use platform's browser API (e.g., `@cloudflare/puppeteer` for Cloudflare Workers) |

### Example: Login Flow Simulation

```bash
# 1. Get credentials from Bitwarden (agent retrieves these)
EMAIL=$(bws secret get <EMAIL_SECRET_ID> -o json | jq -r '.value')
PASSWORD=$(bws secret get <PASSWORD_SECRET_ID> -o json | jq -r '.value')

# 2. Use with agent-browser to:
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$EMAIL"      # Fill email field
agent-browser fill @e2 "$PASSWORD"   # Fill password field
agent-browser click @e3              # Click submit
agent-browser snapshot -i            # Verify authenticated state
```

### Integration with Project Tools

| Project Tool | Integration |
|--------------|-------------|
| **agent-browser** | Use retrieved credentials to fill login forms, authenticate users |
| **Cloud-native browser** (serverless) | Same workflow, using platform's browser API |
| **Supabase MCP** | Retrieve service keys, connection strings for database operations |
| **API Testing** | Inject API keys into request headers |
| **E2E Tests** | Provide test user credentials for authenticated flows |

## CRITICAL: Agent Limitations

**NEVER ask the user for actual secret values or access tokens.** Instead:
1. Guide them through commands they run themselves
2. Provide exact command syntax with placeholders
3. Explain what each step does

The agent must NOT:
- Ask "what is your access token?"
- Request users paste secrets into the chat
- Store or process actual secret values

## Prerequisites

The agent should verify these are set up:

```bash
# Check bws is installed
bws --version

# Check access token is available (don't show the value!)
echo ${BWS_ACCESS_TOKEN:+Access token is set}
```

## macOS Keychain Integration

The BWS access token can be stored securely in macOS Keychain under the service name `bws-access-token`:

```bash
# Store the token in Keychain (user runs this once)
security add-generic-password -a "$USER" -s "bws-access-token" -w "your-token-here"

# Retrieve and export as environment variable
export BWS_ACCESS_TOKEN=$(security find-generic-password -a "$USER" -s "bws-access-token" -w)
```

**For persistent use**, add this line to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export BWS_ACCESS_TOKEN=$(security find-generic-password -a "$USER" -s "bws-access-token" -w 2>/dev/null)
```

This approach:
- Stores the token encrypted in macOS Keychain (protected by login credentials)
- Makes it automatically available in new terminal sessions
- Avoids plain-text secrets in config files

## Inputs the Agent Should Ask For (only if missing)
- **Project name**: Which Bitwarden project to use (e.g., "vibetracking.dev")
- **Secret names**: What secrets are needed (e.g., `SUPABASE_URL`, `API_KEY`)
- **Target env file**: Where to store secrets locally (e.g., `.env.vibetracking`)

## Outputs / Definition of Done
- Secrets retrieved and available for use
- Local `.env` file created/updated (encrypted with dotenvx if needed)
- Verification that secrets are accessible

## Procedure

### 1. List Available Projects

```bash
bws project list
```

This shows all projects the machine account can access.

### 2. List Secrets in a Project

```bash
# Get project ID first
bws project list --output json | jq '.[] | select(.name == "PROJECT_NAME") | .id'

# List secrets in that project
bws secret list <PROJECT_ID>
```

### 3. Retrieve a Specific Secret

```bash
# Get full secret object
bws secret get <SECRET_ID>

# Get just the value (useful for scripts)
bws secret get <SECRET_ID> --output json | jq -r '.value'
```

### 4. Inject Secrets into Commands (Recommended)

The `bws run` command injects all project secrets as environment variables:

```bash
# Run a command with secrets injected
bws run --project-id <PROJECT_ID> -- npm run dev

# Run with specific shell
bws run --project-id <PROJECT_ID> --shell zsh -- './start.sh'

# Don't inherit current environment (isolated)
bws run --project-id <PROJECT_ID> --no-inherit-env -- node server.js
```

### 5. Export Secrets to Local .env File

For projects using dotenvx, create a local encrypted `.env` file:

**Tell the user to run these commands themselves:**

```bash
# Export secrets in env format
bws secret list <PROJECT_ID> --output env > .env.projectname

# Encrypt with dotenvx
dotenvx encrypt -f .env.projectname

# Now the encrypted file can be committed
git add .env.projectname
```

### 6. Sync Workflow: Bitwarden + dotenvx

The recommended pattern for managing secrets:

1. **Bitwarden Secrets Manager** = Central source of truth
2. **dotenvx encrypted .env** = Local cache (can be committed)
3. **BWS_ACCESS_TOKEN** = Stored in dotenvx vault

```bash
# Store access token in dotenvx (user runs this)
cat > .env.bitwarden << 'EOF'
BWS_ACCESS_TOKEN="your-access-token-here"
EOF
dotenvx encrypt -f .env.bitwarden

# Use it to fetch other secrets
dotenvx run -f .env.bitwarden -- bws secret list <PROJECT_ID>
```

## Quick Reference Commands

| Task | Command |
|------|---------|
| List projects | `bws project list` |
| List secrets | `bws secret list [PROJECT_ID]` |
| Get secret | `bws secret get <SECRET_ID>` |
| Get value only | `bws secret get <ID> -o json \| jq -r '.value'` |
| Run with secrets | `bws run --project-id <ID> -- <command>` |
| Export as env | `bws secret list <ID> --output env` |
| Create secret | `bws secret create KEY VALUE PROJECT_ID` |
| Update secret | `bws secret edit <ID> --value "new-value"` |
| Delete secret | `bws secret delete <SECRET_ID>` |

## Example: Setting Up a New Project

When user says "I need to set up Bitwarden secrets for my vibetracking project":

**Respond with:**

> I'll guide you through setting up Bitwarden Secrets Manager. Run these commands yourself:
>
> **Step 1:** List your projects to find the project ID:
> ```bash
> bws project list
> ```
>
> **Step 2:** List secrets in your project:
> ```bash
> bws secret list <PROJECT_ID_FROM_STEP_1>
> ```
>
> **Step 3:** To run your app with secrets injected:
> ```bash
> bws run --project-id <PROJECT_ID> -- npm run dev
> ```
>
> **Step 4:** Or export to a local encrypted file:
> ```bash
> bws secret list <PROJECT_ID> --output env > .env.vibetracking
> dotenvx encrypt -f .env.vibetracking
> ```
>
> Let me know when you've run these and I can help verify the setup!

## Checks & Guardrails
- Never display or log actual secret values
- Use `--output json | jq -r '.value'` for scripts, not direct output
- Verify `BWS_ACCESS_TOKEN` is set before running commands
- Machine accounts have scoped access - verify project permissions
- Rate limits apply when making many requests from same IP

## Agent Workflow: Using Credentials with Browser Automation

When the agent needs to simulate a user login or authenticated action:

### Step 1: Retrieve Credentials
The agent runs bws commands to get the credentials into environment variables:
```bash
# Agent executes this to get credentials
bws secret get <SECRET_ID> -o json | jq -r '.value'
```

### Step 2: Use agent-browser for Automation

```bash
# Navigate to login page
agent-browser open https://app.example.com/login

# Get page structure and element refs
agent-browser snapshot -i

# Fill credentials (using retrieved values)
agent-browser fill @e1 "<email>"
agent-browser fill @e2 "<password>"

# Submit
agent-browser click @e3

# Verify authenticated state
agent-browser snapshot -i
```

### Step 3: Continue Authenticated Flow
Once logged in, the agent can:
- Navigate protected pages
- Fill forms with user data
- Test user-specific features
- Verify permissions and access

### Example: Complete Login Simulation

```
Agent retrieves: EMAIL=user@example.com, PASSWORD=***

1. agent-browser open https://app.example.com/login
2. agent-browser snapshot -i  # Get form field refs
3. agent-browser fill @e1 "<retrieved email>"
4. agent-browser fill @e2 "<retrieved password>"
5. agent-browser click @e3  # Login button
6. agent-browser snapshot -i  # Verify dashboard loaded
```

## References
- [bws Commands Reference](references/bws-commands.md)
- [Integration Patterns](references/integration-patterns.md)
