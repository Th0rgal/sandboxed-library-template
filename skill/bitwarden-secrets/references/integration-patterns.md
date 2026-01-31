# Bitwarden Secrets Manager Integration Patterns

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              Bitwarden Secrets Manager                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Project A  │  │  Project B  │  │  Project C  │     │
│  │  (prod)     │  │  (staging)  │  │  (dev)      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└────────────────────────┬────────────────────────────────┘
                         │ BWS_ACCESS_TOKEN
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    Local Machine                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ .env.bitwarden (encrypted with dotenvx)         │   │
│  │ BWS_ACCESS_TOKEN="encrypted:..."                │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ bws run / bws secret get                        │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Application (secrets as env vars)               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Pattern 1: Direct Injection with `bws run`

**Best for:** Applications that read from environment variables.

```bash
# Run your app with all project secrets injected
bws run --project-id <PROJECT_ID> -- npm run dev
```

**Pros:**
- Secrets never touch disk
- Simple one-liner
- Works with any application

**Cons:**
- Requires bws installed everywhere
- Needs network access to Bitwarden

## Pattern 2: Bitwarden + dotenvx (Recommended)

**Best for:** Teams, offline development, CI/CD.

### Setup Flow

```bash
# 1. Store access token encrypted locally
cat > .env.bitwarden << 'EOF'
BWS_ACCESS_TOKEN="your-machine-account-token"
EOF
dotenvx encrypt -f .env.bitwarden

# 2. Export project secrets to encrypted local file
dotenvx run -f .env.bitwarden -- \
  bws secret list <PROJECT_ID> --output env > .env.myproject
dotenvx encrypt -f .env.myproject

# 3. Commit encrypted files (safe)
git add .env.bitwarden .env.myproject

# 4. Run with local cached secrets
dotenvx run -f .env.myproject -- npm run dev
```

### Refresh Secrets Script

```bash
#!/bin/bash
# refresh-secrets.sh - Update local secrets from Bitwarden

PROJECT_ID="your-project-id"
ENV_FILE=".env.myproject"

# Fetch latest from Bitwarden
dotenvx run -f .env.bitwarden -- \
  bws secret list $PROJECT_ID --output env > $ENV_FILE

# Re-encrypt
dotenvx encrypt -f $ENV_FILE

echo "Secrets refreshed from Bitwarden"
```

## Pattern 3: CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install bws
        run: curl -sSL https://bitwarden.com/secrets/install | sh

      - name: Deploy with secrets
        env:
          BWS_ACCESS_TOKEN: ${{ secrets.BWS_ACCESS_TOKEN }}
        run: |
          bws run --project-id ${{ vars.PROJECT_ID }} -- ./deploy.sh
```

### Docker

```dockerfile
# Multi-stage build - secrets only during build
FROM node:20 AS builder
ARG BWS_ACCESS_TOKEN
RUN curl -sSL https://bitwarden.com/secrets/install | sh
RUN bws run -- npm run build

# Production image - no secrets
FROM node:20-slim
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

## Pattern 4: Multiple Environments

```bash
# Different projects for different environments
bws run --project-id $PROD_PROJECT_ID -- ./deploy-prod.sh
bws run --project-id $STAGING_PROJECT_ID -- ./deploy-staging.sh

# Or use profiles
bws config server-base https://vault.bitwarden.com --profile prod
bws config server-base https://vault.bitwarden.eu --profile eu
bws secret list --profile prod
```

## Pattern 5: Script Integration

### Get Single Secret

```bash
#!/bin/bash
# Get a specific secret value
DB_URL=$(bws secret get <SECRET_ID> --output json | jq -r '.value')
export DB_URL
```

### Bulk Export

```bash
#!/bin/bash
# Export all secrets to environment
eval $(bws secret list <PROJECT_ID> --output env)
# Now all secrets are available as $VAR_NAME
```

### Selective Export

```bash
#!/bin/bash
# Get specific secrets by key name
PROJECT_ID="abc123"

get_secret() {
  bws secret list $PROJECT_ID --output json | \
    jq -r ".[] | select(.key == \"$1\") | .value"
}

export DB_URL=$(get_secret "DATABASE_URL")
export API_KEY=$(get_secret "API_KEY")
```

## Security Best Practices

### 1. Scope Machine Accounts
- Create separate machine accounts per environment
- Use minimal required permissions (read-only if possible)

### 2. Rotate Access Tokens
- Regularly rotate BWS_ACCESS_TOKEN
- Update encrypted storage after rotation

### 3. Don't Log Secrets
```bash
# Bad - logs secret value
echo "Using API key: $API_KEY"

# Good - confirms secret exists without logging value
echo "API key is ${API_KEY:+set}"
```

### 4. Use `bws run` Over Manual Export
```bash
# Preferred - secrets in memory only
bws run -- npm start

# Avoid if possible - secrets touch disk
bws secret list --output env > .env
```

### 5. Encrypt Local Caches
Always encrypt any locally cached secrets with dotenvx:
```bash
bws secret list <ID> --output env > .env.project
dotenvx encrypt -f .env.project
rm -P .env.project.bak  # Securely delete any backups
```

## Troubleshooting

### "Access token invalid"
- Verify token hasn't expired
- Check token has access to the project
- Ensure no whitespace in token

### "Rate limited"
- Use `bws run` to batch secret injection
- Add delays between requests in scripts
- Consider caching with dotenvx

### "Secret not found"
- Verify secret ID with `bws secret list`
- Check machine account has access to project
- Confirm project ID is correct

### Non-POSIX Secret Names
If secrets have names with hyphens or special characters:
```bash
# Use UUID-based variable names
bws run --uuids-as-keynames -- 'echo $_64246aa4_70b3_4332_8587_8b1284ce6d76'

# Or rename secrets to use underscores only
bws secret edit <ID> --key "MY_API_KEY"  # Instead of "my-api-key"
```
