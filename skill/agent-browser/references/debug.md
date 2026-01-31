# Debug & Recording Reference

## Console Messages

View JavaScript console output.
```bash
agent-browser console
agent-browser console --clear    # View and clear
agent-browser console --json
```

## Page Errors

View JavaScript errors.
```bash
agent-browser errors
agent-browser errors --clear
agent-browser errors --json
```

## Element Highlighting

Visually highlight elements for debugging.
```bash
agent-browser highlight @e1
agent-browser highlight "#submit-btn"
```

## Trace Recording

Record Playwright trace for debugging.
```bash
agent-browser trace start
# ... perform actions ...
agent-browser trace stop trace.zip
```

## Video Recording

Record browser session as WebM video.
```bash
agent-browser record start video.webm
agent-browser record start video.webm https://example.com  # Start with URL
# ... perform actions ...
agent-browser record stop
agent-browser record restart ./take2.webm  # Stop current + start new
```

Recording creates a fresh context but preserves cookies/storage from your session.
If no URL is provided, it automatically returns to your current page.
For smooth demos, explore first, then start recording.

## Debug Mode

Enable verbose debug output.
```bash
agent-browser --debug open example.com
agent-browser --debug snapshot
```

## Headed Mode

Show browser window (not headless).
```bash
agent-browser --headed open example.com
```

## CDP Connection

Connect to existing browser via Chrome DevTools Protocol.
```bash
# Connect to CDP port
agent-browser --cdp 9222 snapshot

# Connect to CDP URL
agent-browser connect 9222
agent-browser connect ws://localhost:9222/devtools/browser/...
```

## Session Management

### View current session
```bash
agent-browser session
```

### List active sessions
```bash
agent-browser session list
```

### Use named sessions
```bash
agent-browser --session test open example.com
agent-browser --session test snapshot
agent-browser --session prod open prod.example.com
```

Sessions are isolated with separate cookies, storage, and browser state.

## Persistent Profiles

Use persistent browser profile that survives restarts.
```bash
agent-browser --profile ~/.myapp open example.com
```

## Load Storage State

Load cookies and storage from a JSON file.
```bash
agent-browser --state auth-state.json open example.com
```

## Save and Restore State

```bash
agent-browser state save auth.json   # Save current cookies/storage
agent-browser state load auth.json   # Load saved state into session
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_BROWSER_SESSION` | Default session name |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser executable |
| `AGENT_BROWSER_PROVIDER` | Cloud browser provider |
| `AGENT_BROWSER_STREAM_PORT` | WebSocket streaming port |
| `AGENT_BROWSER_ARGS` | Browser launch args |
| `AGENT_BROWSER_USER_AGENT` | Custom User-Agent |
| `AGENT_BROWSER_PROXY` | Proxy server URL |
| `AGENT_BROWSER_PROXY_BYPASS` | Hosts to bypass proxy |
| `AGENT_BROWSER_PROFILE` | Persistent profile path |
| `AGENT_BROWSER_STATE` | Storage state file path |
| `AGENT_BROWSER_HOME` | Custom install location |
| `AGENT_BROWSER_EXTENSIONS` | Comma-separated extension paths |

## Browser Installation

Install browser binaries.
```bash
agent-browser install
agent-browser install --with-deps  # Include system deps (Linux)
```

## Custom Browser

Use custom browser executable.
```bash
agent-browser --executable-path /path/to/chrome open example.com
```

## Browser Extensions

Load browser extensions.
```bash
agent-browser --extension /path/to/extension open example.com
agent-browser --extension ext1 --extension ext2 open example.com
```

## Browser Launch Arguments

Pass custom args to browser.
```bash
agent-browser --args "--no-sandbox,--disable-blink-features=AutomationControlled" open example.com
```

## HTTPS Certificate Errors

For sites with self-signed or invalid certificates:
```bash
agent-browser open https://localhost:8443 --ignore-https-errors
```
