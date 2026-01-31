# bws CLI Commands Reference

## Installation

```bash
# Using installation script (recommended)
curl -sSL https://bitwarden.com/secrets/install | sh

# Using Cargo (if Rust installed)
cargo install bws

# Manual download from GitHub releases
# https://github.com/bitwarden/sdk-sm/releases
```

## Authentication

### Environment Variable (Recommended)
```bash
export BWS_ACCESS_TOKEN="your-access-token"
```

### Inline Token
```bash
bws secret list --access-token "your-access-token"
```

### With dotenvx
```bash
dotenvx run -f .env.bitwarden -- bws secret list
```

## Secret Commands

### List Secrets
```bash
# List all accessible secrets
bws secret list

# List secrets in specific project
bws secret list <PROJECT_ID>

# Output formats
bws secret list --output json
bws secret list --output yaml
bws secret list --output table
bws secret list --output env    # KEY=VALUE format
bws secret list --output tsv
```

### Get Secret
```bash
# Get full secret object
bws secret get <SECRET_ID>

# Get as JSON
bws secret get <SECRET_ID> --output json

# Get just the value (script-friendly)
bws secret get <SECRET_ID> --output json | jq -r '.value'
```

### Create Secret
```bash
# Basic creation
bws secret create <KEY> <VALUE> <PROJECT_ID>

# With note/description
bws secret create API_KEY "sk-xxx" abc123 --note "Production API key"
```

### Edit Secret
```bash
# Update value
bws secret edit <SECRET_ID> --value "new-value"

# Update key name
bws secret edit <SECRET_ID> --key "NEW_KEY_NAME"

# Update note
bws secret edit <SECRET_ID> --note "Updated description"

# Move to different project
bws secret edit <SECRET_ID> --project-id <NEW_PROJECT_ID>

# Multiple updates
bws secret edit <SECRET_ID> --key "NEW_NAME" --value "new-val" --note "updated"
```

### Delete Secrets
```bash
# Delete single secret
bws secret delete <SECRET_ID>

# Delete multiple secrets
bws secret delete <ID1> <ID2> <ID3>
```

## Project Commands

### List Projects
```bash
bws project list
bws project list --output json
```

### Get Project
```bash
bws project get <PROJECT_ID>
```

### Create Project
```bash
bws project create "My New Project"
```

### Edit Project
```bash
bws project edit <PROJECT_ID> --name "New Project Name"
```

### Delete Projects
```bash
bws project delete <PROJECT_ID>
bws project delete <ID1> <ID2>
```

## Run Command (Environment Injection)

The `run` command executes commands with secrets injected as environment variables.

```bash
# Basic usage
bws run -- 'npm start'

# From specific project
bws run --project-id <PROJECT_ID> -- 'npm run dev'

# Chain commands
bws run -- 'npm install && npm run build'

# Use specific shell
bws run --shell fish -- './script.sh'
bws run --shell zsh -- 'echo $MY_SECRET'

# Isolated environment (don't inherit current env vars)
bws run --no-inherit-env -- 'node app.js'

# Use UUIDs as variable names (for non-POSIX-compliant secret names)
bws run --uuids-as-keynames -- 'echo $_64246aa4_70b3_4332_8587_8b1284ce6d76'
```

**Security Warning:** Only execute commands you trust. The run command executes commands in your shell.

## Configuration

### Server Configuration
```bash
# Set server URL (default: vault.bitwarden.com)
bws config server-base https://vault.bitwarden.com

# Use profile for different environments
bws config server-base https://vault.bitwarden.eu --profile europe

# Custom config file
bws config server-base https://custom.server --config-file ~/.bws/alt-config
```

### State Directory
```bash
bws config state-dir /path/to/state
```

To opt out of state files, set `state_opt_out: true` in config.

## Output Formats

| Format | Flag | Description |
|--------|------|-------------|
| JSON | `-o json` | Default, full object |
| YAML | `-o yaml` | YAML formatted |
| Table | `-o table` | ASCII table with headers |
| TSV | `-o tsv` | Tab-separated values |
| Env | `-o env` | KEY=VALUE pairs |
| None | `-o none` | Suppress output (errors only) |

## Global Options

| Option | Description |
|--------|-------------|
| `-t, --access-token` | Authenticate with access token |
| `-o, --output` | Output format |
| `--color [yes\|no\|auto]` | Colorized output |
| `--config-file <PATH>` | Custom config file path |
| `--profile <NAME>` | Use named profile |
| `--server-url <URL>` | Override server URL |
| `-h, --help` | Show help |
| `--version` | Show version |

## Useful Patterns

### Export to file
```bash
bws secret list <PROJECT_ID> --output env > .env
```

### Get single value into variable
```bash
export DB_URL=$(bws secret get <ID> -o json | jq -r '.value')
```

### Find project ID by name
```bash
bws project list -o json | jq -r '.[] | select(.name == "myproject") | .id'
```

### Find secret ID by key
```bash
bws secret list <PROJECT_ID> -o json | jq -r '.[] | select(.key == "API_KEY") | .id'
```

## Rate Limits

Making many requests from the same IP in a short time may trigger rate limits. Use the `run` command to inject all secrets at once rather than fetching individually.
