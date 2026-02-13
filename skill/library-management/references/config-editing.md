# Config Profile Editing Guide

This guide explains how to edit configuration profiles in the Open Agent Library.
Config profiles store harness-specific settings that control how agents behave.

## Overview

Config profiles are stored at `configs/<profile-name>/` and contain settings for:
- **Claude Code** (`.claudecode/settings.json`)
- **OpenCode** (`.opencode/settings.json`)
- **Amp Code** (`.ampcode/settings.json`)
- **Sandboxed.sh** (`.sandboxed-sh/config.json`)

## Claude Code Settings (`.claudecode/settings.json`)

Controls Claude Code behavior for missions using this profile.

```json
{
  "default_model": "claude-opus-4-5",
  "default_agent": null,
  "hidden_agents": [],
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `default_model` | string | Default model ID. Options: `"claude-opus-4-5"`, `"claude-sonnet-4-20250514"`, `"claude-haiku-3-5"` |
| `default_agent` | string\|null | Agent to pre-select in new missions |
| `hidden_agents` | string[] | Agents to hide from the mission dialog |
| `attribution.commit` | string | Text added to commits. Empty string `""` disables co-author attribution |
| `attribution.pr` | string | Text added to PRs. Empty string `""` disables PR attribution |

### Common Tasks

**Disable co-author in commits:**
```json
{
  "default_model": "claude-opus-4-5",
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

**Hide system agents:**
```json
{
  "hidden_agents": ["build", "plan", "explore", "compaction"]
}
```

## Sandboxed.sh Settings (`.sandboxed-sh/config.json`)

Controls Sandboxed.sh dashboard behavior.

```json
{
  "hidden_agents": ["build", "plan", "general", "explore"],
  "default_agent": "Sisyphus",
  "desktop": {
    "auto_close_grace_period_secs": 7200,
    "cleanup_interval_secs": 900,
    "warning_before_close_secs": 300
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `hidden_agents` | string[] | Agents hidden from mission dialog selector |
| `default_agent` | string\|null | Agent pre-selected when creating missions |
| `desktop.auto_close_grace_period_secs` | number | Seconds before auto-closing orphaned desktop sessions (default: 7200) |
| `desktop.cleanup_interval_secs` | number | Interval for cleanup sweep (default: 900) |
| `desktop.warning_before_close_secs` | number | Warning notification time before auto-close (default: 300) |

## OpenCode Settings (`.opencode/settings.json`)

OpenCode-specific settings (oh-my-opencode plugin config).

```json
{
  "theme": "default",
  "plugins": ["ralph-wiggum"],
  "auto_compact": true
}
```

## Amp Code Settings (`.ampcode/settings.json`)

Amp Code backend settings.

```json
{
  "default_mode": "smart"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `default_mode` | string\|null | Default mode: `"smart"` or `"rush"` |

## Editing Profiles

### Via Library API Tools

1. **Get current profile:**
   ```
   library-configs_get_profile({ name: "default" })
   ```

2. **Get specific file:**
   ```
   library-configs_get_file({ profile: "default", path: ".claudecode/settings.json" })
   ```

3. **Save file (disable co-author):**
   ```
   library-configs_save_file({
     profile: "default",
     path: ".claudecode/settings.json",
     content: "{\"default_model\": \"claude-opus-4-5\", \"attribution\": {\"commit\": \"\", \"pr\": \"\"}}"
   })
   ```

4. **Commit and push:**
   ```
   library-git_commit({ message: "Disable co-author in commits" })
   library-git_push()
   ```

### Via REST API

```bash
# Get profile
curl https://agent-backend.thomas.md/api/library/config-profile/default

# Update Claude Code settings to disable co-author
curl -X PUT https://agent-backend.thomas.md/api/library/config-profile/default/file/.claudecode/settings.json \
  -H "Content-Type: application/json" \
  -d '{"content": "{\"default_model\": \"claude-opus-4-5\", \"attribution\": {\"commit\": \"\", \"pr\": \"\"}}"}'

# Commit
curl -X POST https://agent-backend.thomas.md/api/library/commit \
  -H "Content-Type: application/json" \
  -d '{"message": "Disable Claude co-author attribution"}'

# Push
curl -X POST https://agent-backend.thomas.md/api/library/push
```

## Creating New Profiles

1. **Create profile:**
   ```
   library-configs_save_profile({ name: "production", is_default: false })
   ```

2. **Copy settings from default:**
   - Get default profile files
   - Save them to the new profile

3. **Customize as needed**

## Profile Selection in Templates

Workspace templates specify which config profile to use:

```json
{
  "name": "my-template",
  "config_profile": "production"
}
```

If `config_profile` is not specified, the `default` profile is used.

## Best Practices

1. **Always get before updating** - Avoid overwriting concurrent changes
2. **Use meaningful commit messages** - Document what changed and why
3. **Test in dev first** - Verify changes on dev backend before production
4. **Keep profiles focused** - Create separate profiles for different use cases