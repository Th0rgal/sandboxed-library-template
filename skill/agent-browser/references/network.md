# Network & Cookies Reference

## Cookies

### Get all cookies
```bash
agent-browser cookies
agent-browser cookies get
agent-browser cookies --json
```

### Set a cookie
```bash
agent-browser cookies set <name> <value> [options]

# Simple cookie for current page
agent-browser cookies set session_id "abc123"

# Set cookie before loading page (for auth)
agent-browser cookies set session_id "abc123" --url https://app.example.com

# Secure cookie with domain and path
agent-browser cookies set auth_token "xyz789" --domain example.com --path /api --httpOnly --secure

# Cookie with SameSite policy
agent-browser cookies set tracking "yes" --sameSite Strict

# Cookie with expiration (Unix timestamp)
agent-browser cookies set temp "123" --expires 1735689600
```

### Cookie options
| Option | Description |
|--------|-------------|
| `--url <url>` | URL for the cookie (set before page load) |
| `--domain <domain>` | Cookie domain (e.g., ".example.com") |
| `--path <path>` | Cookie path (e.g., "/api") |
| `--httpOnly` | Prevent JavaScript access |
| `--secure` | HTTPS only |
| `--sameSite <policy>` | Strict, Lax, or None |
| `--expires <timestamp>` | Unix timestamp in seconds |

### Clear cookies
```bash
agent-browser cookies clear
```

## Web Storage

### Local storage
```bash
agent-browser storage local              # Get all
agent-browser storage local get <key>    # Get value
agent-browser storage local set <k> <v>  # Set value
agent-browser storage local remove <key> # Remove key
agent-browser storage local clear        # Clear all
```

### Session storage
```bash
agent-browser storage session            # Get all
agent-browser storage session get <key>
agent-browser storage session set <k> <v>
agent-browser storage session remove <key>
agent-browser storage session clear
```

## Network Interception

### Route requests
Intercept and modify network requests.
```bash
# Abort requests matching pattern
agent-browser network route "**/api/*" --abort

# Mock response
agent-browser network route "**/data.json" --body '{"mock": true}'
```

### Remove routes
```bash
agent-browser network unroute             # Remove all routes
agent-browser network unroute "**/api/*"  # Remove specific route
```

### View captured requests
```bash
agent-browser network requests
agent-browser network requests --filter "api"
agent-browser network requests --clear
agent-browser network requests --json
```

## HTTP Headers

Set extra HTTP headers (scoped to origin).
```bash
agent-browser set headers '{"Authorization": "Bearer token123"}'
agent-browser set headers '{"X-Custom-Header": "value"}'

# Or via --headers option
agent-browser --headers '{"Authorization": "Bearer token"}' open app.example.com
```

## HTTP Authentication

```bash
agent-browser set credentials <username> <password>
agent-browser set credentials admin secret123
```
Alias: `set auth`

## Proxy Configuration

```bash
# Via command option
agent-browser --proxy "http://127.0.0.1:7890" open example.com
agent-browser --proxy "http://user:pass@127.0.0.1:7890" open example.com
agent-browser --proxy "socks5://proxy.com:1080" open example.com

# Bypass proxy for hosts
agent-browser --proxy-bypass "localhost,*.internal.com" open example.com

# Via environment variable
AGENT_BROWSER_PROXY="http://127.0.0.1:7890" agent-browser open example.com
AGENT_BROWSER_PROXY_BYPASS="localhost" agent-browser open example.com
```
