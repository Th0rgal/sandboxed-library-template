# dotenvx Vault Architecture

## File Structure

For a repo named `relens-ai`:

```
relens-ai/
├── .env.relens_ai         # Encrypted env file (commit this)
├── .env.keys              # Private keys (NEVER commit)
└── .gitignore             # Must include .env.keys
```

## Naming Convention (CRITICAL)

All naming derives from the **git repository name**:

| Repo Name | .env File | Private Key Variable |
|-----------|-----------|---------------------|
| `relens-ai` | `.env.relens_ai` | `DOTENV_PRIVATE_KEY_RELENS_AI` |
| `vibe-tracking` | `.env.vibe_tracking` | `DOTENV_PRIVATE_KEY_VIBE_TRACKING` |
| `my_app` | `.env.my_app` | `DOTENV_PRIVATE_KEY_MY_APP` |

**Rules:**
- Replace hyphens (`-`) with underscores (`_`)
- `.env` file uses lowercase: `.env.repo_name`
- Key variable uses UPPERCASE: `DOTENV_PRIVATE_KEY_REPO_NAME`

## Encryption Flow

```
┌─────────────────┐
│ Plaintext .env  │
│ API_KEY="abc"   │
└────────┬────────┘
         │ dotenvx encrypt -f .env.relens_ai
         ▼
┌─────────────────────────────────────────┐
│ Encrypted .env.relens_ai                │
│ API_KEY="encrypted:BO3Qm..."            │
└─────────────────────────────────────────┘
         │
         │ (generates)
         ▼
┌─────────────────────────────────────────┐
│ .env.keys                               │
│ DOTENV_PRIVATE_KEY_RELENS_AI="xyz..."   │
└─────────────────────────────────────────┘
```

## Key Naming Convention

Private keys in `.env.keys` are derived from the **repo name**:
- Repo `relens-ai` → `DOTENV_PRIVATE_KEY_RELENS_AI` for `.env.relens_ai`
- Repo `vibe-tracking` → `DOTENV_PRIVATE_KEY_VIBE_TRACKING` for `.env.vibe_tracking`

The suffix is the repo name in UPPERCASE with hyphens converted to underscores.

## Security Model

### What to Commit
- Encrypted `.env.repo_name` files (safe to commit)

### What to NEVER Commit
- `.env.keys` (contains private decryption keys)
- Plaintext `.env` files with real secrets

### Sharing Keys
1. **Global keys file**: Store in `~/.dotenvx/keys` (recommended)
2. **Password manager**: Store keys in 1Password, Bitwarden, etc.
3. **CI secrets**: Set `DOTENV_PRIVATE_KEY_REPO_NAME` as environment variable

## Repo-Based Setup (Recommended)

For a repo named `relens-ai`:

```bash
# Single env file per repo, named after the repo
.env.relens_ai      # Encrypted secrets for this repo

# Key in ~/.dotenvx/keys:
export DOTENV_PRIVATE_KEY_RELENS_AI="..."
```

For multi-environment repos, append the environment:

```bash
.env.relens_ai_dev         # Dev secrets
.env.relens_ai_staging     # Staging secrets
.env.relens_ai_prod        # Production secrets

# Keys:
DOTENV_PRIVATE_KEY_RELENS_AI_DEV="..."
DOTENV_PRIVATE_KEY_RELENS_AI_STAGING="..."
DOTENV_PRIVATE_KEY_RELENS_AI_PROD="..."
```

## Runtime Decryption

When running `dotenvx run -f .env.relens_ai -- command`:

1. dotenvx reads `.env.relens_ai` (encrypted)
2. Looks for `DOTENV_PRIVATE_KEY_RELENS_AI` in:
   - Current environment (from `~/.dotenvx/keys` via shell profile)
   - `.env.keys` file (local fallback)
3. Decrypts values in memory
4. Injects into process environment
5. Runs the command

**Note:** Decrypted values never touch disk during `run`.

## Backup Strategy

Store keys in `~/.dotenvx/keys` with proper permissions. Back up this file:

1. **Password manager** (recommended)
   - Store entire `~/.dotenvx/keys` content as a secure note

2. **Encrypted cloud storage**
   - Encrypt with GPG before uploading

3. **Hardware security key**
   - For high-security environments

## Troubleshooting

### "Missing private key" error
```bash
# Check if key exists in global keys
grep DOTENV_PRIVATE_KEY ~/.dotenvx/keys

# Ensure correct naming based on repo
# Repo: relens-ai
# File: .env.relens_ai
# Key:  DOTENV_PRIVATE_KEY_RELENS_AI
```

### Can't decrypt after pulling repo
1. Ensure key is in `~/.dotenvx/keys`
2. Check key name matches repo name (UPPERCASE, underscores)
3. Verify shell profile sources `~/.dotenvx/keys`

### Re-encrypting with new key
```bash
# Decrypt with old key
dotenvx decrypt -f .env.relens_ai > .env.relens_ai.tmp

# Remove old key from ~/.dotenvx/keys
# (manually edit to remove DOTENV_PRIVATE_KEY_RELENS_AI)

# Re-encrypt (generates new key)
mv .env.relens_ai.tmp .env.relens_ai
dotenvx encrypt -f .env.relens_ai

# Add new key to global keys
cat .env.keys >> ~/.dotenvx/keys
rm .env.keys
```
