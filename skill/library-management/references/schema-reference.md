# Library Entity Schema Reference

Complete JSON schemas for all library entity types.

## Workspace Template Schema

Location: `workspace-template/<name>.json`

```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "distro": "string (optional, e.g., \"ubuntu-noble\")",
  "skills": ["string array - skill names to include"],
  "env_vars": {
    "KEY": "value (strings, sensitive values auto-encrypted)"
  },
  "encrypted_keys": ["string array - keys of env_vars to encrypt"],
  "init_scripts": ["string array - init script fragment names, executed in order"],
  "init_script": "string - custom bash appended after fragments",
  "shared_network": "boolean|null - true=share host network, false=isolated, null=default(true)",
  "tailscale_mode": "\"exit_node\"|\"tailnet_only\"|null - when shared_network=false",
  "mcps": ["string array - MCP server names to enable"],
  "config_profile": "string|null - config profile name (default: \"default\")"
}
```

### Example

```json
{
  "name": "my-workspace",
  "description": "Development workspace with browser support",
  "distro": "ubuntu-noble",
  "skills": ["github-cli", "library-management"],
  "env_vars": {
    "DISPLAY": ":99",
    "API_KEY": "secret-value"
  },
  "encrypted_keys": ["API_KEY"],
  "init_scripts": ["base", "ssh-keys", "git-config", "browser-x11"],
  "init_script": "npm install -g typescript",
  "shared_network": null,
  "mcps": ["playwright"],
  "config_profile": "default"
}
```

## Skill Schema

Location: `skill/<name>/SKILL.md`

```yaml
---
name: string (required)
description: string (required, include trigger terms)
setup_commands: [string array - shell commands run during workspace setup]
---

Markdown body with instructions...
```

Recommended body sections (improve routing and reliability):
- `## Use when` - Positive trigger cases
- `## Don't use when` - Negative examples to prevent misfires
- `## Outputs` - Expected file outputs or formats (use `artifacts/` as the default boundary)
- `## Instructions` - The core procedure
- `## Templates or Examples` - Worked examples and output templates (loaded only when the skill is used)

### Skill Files

Skills can contain additional reference files:
- `references/*.md` - Supporting documentation
- `scripts/*.py` - Executable scripts
- Any other files needed by the skill

## Agent Schema

Location: `agent/<name>.md`

```yaml
---
description: string (required)
mode: "primary"|"subagent" (optional)
model: string (optional, e.g., "anthropic/claude-sonnet-4-20250514")
hidden: boolean (optional, default: false)
color: string (optional, hex color e.g., "#44BA81")
tools:
  "*": boolean - default for all tools
  "tool-name": boolean - override for specific tool
permission:
  edit: "ask"|"allow"|"deny"
  bash:
    "*": "ask"|"allow"|"deny"
    "npm *": "allow"
rules:
  - rule-name
---

Agent system prompt in markdown...
```

### Example

```yaml
---
description: Code review specialist
mode: subagent
model: anthropic/claude-sonnet-4-20250514
hidden: false
color: "#4A90D9"
tools:
  "*": false
  "read": true
  "grep": true
  "glob": true
permission:
  edit: deny
  bash:
    "*": deny
rules:
  - code-style
---

You are a code review specialist...
```

## Command Schema

Location: `command/<name>.md`

```yaml
---
description: string (required)
model: string (optional)
subtask: boolean (optional, run as subtask)
agent: string (optional, agent to use)
params:
  - name: string
    required: boolean
    description: string
---

Command prompt template.
Use $ARGUMENTS for user input.
Use $PARAM_NAME for specific parameters.
```

### Example

```yaml
---
description: Review a pull request
params:
  - name: pr-number
    required: true
    description: The PR number to review
---

Review pull request #$PR_NUMBER focusing on:
1. Code quality
2. Security issues
3. Performance concerns
```

## Rule Schema

Location: `rule/<name>.md`

```yaml
---
description: string (required)
---

Rule instructions applied to agents referencing this rule.
```

## Init Script Schema

Location: `init-script/<name>/SCRIPT.sh`

```bash
#!/usr/bin/env bash
# Description: Brief description of what this fragment does

set -euo pipefail

# Logging setup (optional but recommended)
LOG=/var/log/openagent-init.log
exec > >(tee -a "$LOG") 2>&1
trap 'echo "Init failed at line $LINENO: $BASH_COMMAND" >&2' ERR

export DEBIAN_FRONTEND=noninteractive

# Retry helper (optional)
retry() {
  local n=0
  local max="${RETRY_MAX:-5}"
  until "$@"; do
    n=$((n+1))
    [ "$n" -ge "$max" ] && return 1
    sleep 2
  done
}

# Your setup commands here
```

## MCP Server Schema

Location: `mcp/servers.json`

```json
{
  "server-name": {
    "type": "local",
    "command": ["npx", "@package/mcp-server"],
    "env": {
      "ENV_VAR": "value"
    },
    "enabled": true
  },
  "remote-server": {
    "type": "remote",
    "url": "https://mcp.example.com",
    "headers": {
      "Authorization": "Bearer token"
    },
    "enabled": true
  }
}
```

## Config Profile Schema

Location: `configs/<profile>/`

### Directory Structure

```
configs/<profile>/
├── .claudecode/
│   └── settings.json
├── .opencode/
│   └── settings.json
├── .ampcode/
│   └── settings.json
└── .sandboxed-sh/
    └── config.json
```

### Claude Code Settings

```json
{
  "default_model": "claude-opus-4-5",
  "default_agent": null,
  "hidden_agents": [],
  "commit_co_author": true
}
```

### Sandboxed.sh Config

```json
{
  "hidden_agents": ["build", "plan", "explore"],
  "default_agent": "Sisyphus",
  "desktop": {
    "auto_close_grace_period_secs": 7200,
    "cleanup_interval_secs": 900,
    "warning_before_close_secs": 300
  }
}
```

### Amp Code Settings

```json
{
  "default_mode": "smart"
}
```

## Plugin Schema

Location: `plugins.json`

```json
{
  "plugin-name": {
    "package": "npm-package-name",
    "description": "What this plugin does",
    "enabled": true,
    "ui": {
      "icon": "lucide-icon-name",
      "label": "Display Name",
      "hint": "Short hint",
      "category": "automation"
    }
  }
}
```

## Validation Notes

1. **Names**: Lowercase, hyphens allowed, 1-64 characters
2. **Descriptions**: Required for most entities, include trigger terms for skills
3. **YAML Frontmatter**: Must have `---` delimiters
4. **JSON**: Must be valid JSON (no trailing commas)
5. **Encrypted Values**: Marked with `<encrypted v="1">...</encrypted>` tags
