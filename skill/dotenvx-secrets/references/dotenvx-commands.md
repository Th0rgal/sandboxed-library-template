# dotenvx Commands Reference

## Naming Convention

All file and key naming derives from the **git repository name**:

```bash
# Get repo name
REPO_NAME=$(basename $(git rev-parse --show-toplevel) | tr '-' '_')

# Example for relens-ai repo:
# .env file: .env.relens_ai
# Key var:   DOTENV_PRIVATE_KEY_RELENS_AI
```

## Core Commands

### encrypt
Encrypt a `.env` file in place.

```bash
# Encrypt repo-specific file (recommended)
dotenvx encrypt -f .env.relens_ai

# Encrypt multiple files
dotenvx encrypt -f .env.relens_ai_dev -f .env.relens_ai_prod
```

### decrypt
Decrypt an encrypted `.env` file (requires keys).

```bash
# Decrypt to stdout
dotenvx decrypt -f .env.relens_ai

# Decrypt to file
dotenvx decrypt -f .env.relens_ai > .env.relens_ai.decrypted
```

### run
Run a command with decrypted environment variables.

```bash
# With repo-specific env file
dotenvx run -f .env.relens_ai -- npm start

# With specific env file
dotenvx run -f .env.relens_ai -- node server.js

# Multiple env files (later files override earlier)
dotenvx run -f .env.relens_ai -f .env.local -- npm run dev

# Override specific variable
dotenvx run -f .env.relens_ai -- env VAR=override npm start
```

### set
Set a single environment variable (encrypts automatically).

```bash
dotenvx set KEY value -f .env.relens_ai
```

### get
Get a decrypted value.

```bash
dotenvx get KEY -f .env.relens_ai
```

## Flags Reference

| Flag | Description |
|------|-------------|
| `-f, --env-file` | Specify env file(s) to use |
| `--overload` | Override existing env vars |
| `-q, --quiet` | Suppress output |
| `--debug` | Enable debug logging |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `DOTENV_PRIVATE_KEY` | Default private key for decryption |
| `DOTENV_PRIVATE_KEY_<REPO_NAME>` | Per-repo private key (e.g., `DOTENV_PRIVATE_KEY_RELENS_AI`) |

## Common Patterns

### Development workflow
```bash
# Encrypt after editing (repo: relens-ai)
dotenvx encrypt -f .env.relens_ai

# Run dev server
dotenvx run -f .env.relens_ai -- npm run dev
```

### CI/CD
```bash
# Set DOTENV_PRIVATE_KEY_RELENS_AI as CI secret, then:
dotenvx run -f .env.relens_ai -- npm run build
```

### Adding new secret
```bash
# 1. Decrypt existing file
dotenvx decrypt -f .env.relens_ai > .env.relens_ai.tmp

# 2. Add new secret to .env.relens_ai.tmp

# 3. Replace and re-encrypt
mv .env.relens_ai.tmp .env.relens_ai
dotenvx encrypt -f .env.relens_ai
```
