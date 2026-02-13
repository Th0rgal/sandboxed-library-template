---
name: library-management
description: >
  Manage the Open Agent library (skills, agents, commands, tools, rules, MCPs, workspace templates, config profiles) via Library API tools.
  Trigger terms: library, skill, agent, command, tool, rule, MCP, template, save skill, create skill, config profile, configs.
---

# Open Agent Library Management

The Open Agent Library is a Git-backed configuration repo that stores reusable skills, agents,
commands, tools, rules, MCP servers, workspace templates, and config profiles. Use the `library-*` tools to
read and update that repo.

## Use when
- Creating or updating skills, agents, commands, tools, rules, or MCPs
- Managing workspace templates
- Editing config profiles (Claude Code settings, harness configs)
- Adding reference files to skills (examples, templates, supporting docs)
- Syncing library git state (status/sync/commit/push)

## Don't use when
- Local file operations unrelated to the library
- Running missions or managing workspace lifecycle

## Outputs
- Updated library files and git commits (store exports in `artifacts/` if needed).

## Templates or Examples
- Use the tool maps below as templates for calling library tools.

## Tool Map (file name + export)
Tool names follow the pattern `<filename>_<export>`.

### Skills (`library-skills.ts`)
- `library-skills_list_skills`
- `library-skills_get_skill`
- `library-skills_save_skill`
- `library-skills_delete_skill`
- `library-skills_get_skill_file` - Get a reference file within a skill folder
- `library-skills_save_skill_file` - Save a reference file within a skill folder
- `library-skills_delete_skill_file` - Delete a reference file from a skill folder

### Agents (`library-agents.ts`)
- `library-agents_list_agents`
- `library-agents_get_agent`
- `library-agents_save_agent`
- `library-agents_delete_agent`

### Commands / Tools / Rules (`library-commands.ts`)
- Commands: `library-commands_list_commands`, `library-commands_get_command`, `library-commands_save_command`, `library-commands_delete_command`
- Tools: `library-commands_list_tools`, `library-commands_get_tool`, `library-commands_save_tool`, `library-commands_delete_tool`
- Rules: `library-commands_list_rules`, `library-commands_get_rule`, `library-commands_save_rule`, `library-commands_delete_rule`

### Workspace Templates (`library-templates.ts`)
- `library-templates_list_templates`
- `library-templates_get_template`
- `library-templates_save_template`
- `library-templates_delete_template`

### Config Profiles (`library-configs.ts`)
- `library-configs_list_profiles`
- `library-configs_get_profile`
- `library-configs_save_profile`
- `library-configs_delete_profile`
- `library-configs_get_file` - Get a specific file within a profile
- `library-configs_save_file` - Save a specific file within a profile

### MCPs + Git (`library-git.ts`)
- MCPs: `library-git_get_mcps`, `library-git_save_mcps`
- Git: `library-git_status`, `library-git_sync`, `library-git_commit`, `library-git_push`

## Quick Reference

| Resource | List | Get | Save | Delete |
|----------|------|-----|------|--------|
| Skills | `library-skills_list_skills` | `library-skills_get_skill` | `library-skills_save_skill` | `library-skills_delete_skill` |
| Skill Files | (via get_skill) | `library-skills_get_skill_file` | `library-skills_save_skill_file` | `library-skills_delete_skill_file` |
| Agents | `library-agents_list_agents` | `library-agents_get_agent` | `library-agents_save_agent` | `library-agents_delete_agent` |
| Commands | `library-commands_list_commands` | `library-commands_get_command` | `library-commands_save_command` | `library-commands_delete_command` |
| Tools | `library-commands_list_tools` | `library-commands_get_tool` | `library-commands_save_tool` | `library-commands_delete_tool` |
| Rules | `library-commands_list_rules` | `library-commands_get_rule` | `library-commands_save_rule` | `library-commands_delete_rule` |
| Templates | `library-templates_list_templates` | `library-templates_get_template` | `library-templates_save_template` | `library-templates_delete_template` |
| Config Profiles | `library-configs_list_profiles` | `library-configs_get_profile` | `library-configs_save_profile` | `library-configs_delete_profile` |
| MCPs | - | `library-git_get_mcps` | `library-git_save_mcps` | - |

## Procedure

1. **List** existing items to see what's there
2. **Get** current content before editing
3. **Save** the full updated content (frontmatter + body)
4. **Commit** with a clear message
5. **Push** to sync the library remote

## Procedure References

For detailed guides on specific operations, see these reference files:
- `references/config-editing.md` - How to edit config profiles (Claude Code settings, etc.)
- `references/schema-reference.md` - JSON schemas for all library entity types

## File Formats

### Skill (`skill/<name>/SKILL.md`)
```yaml
---
name: skill-name
description: What this skill does (include trigger terms)
---

## Use when
- ...

## Don't use when
- ...

## Outputs
- Expected files in `artifacts/` or required formats

## Instructions
...

## Templates or Examples
...
```

Skills can also contain reference files (examples, templates, supporting docs) in the same folder.
Use `library-skills_save_skill_file` to add files like `skill/<name>/example.md`.

### Agent (`agent/<name>.md`)
```yaml
---
description: Agent description
mode: primary | subagent
model: provider/model-id
hidden: true | false
color: "#44BA81"
tools:
  "*": false
  "read": true
  "write": true
permission:
  edit: ask | allow | deny
  bash:
    "*": ask
rules:
  - rule-name
---
Agent system prompt...
```

### Command (`command/<name>.md`)
```yaml
---
description: Command description
model: provider/model-id
subtask: true | false
agent: agent-name
---
Command prompt template. Use $ARGUMENTS for user input.
```

### Tool (`tool/<name>.ts`)
```typescript
import { tool } from "@opencode-ai/plugin"

export const my_tool = tool({
  description: "What it does",
  args: { param: tool.schema.string().describe("Param description") },
  async execute(args) {
    return "result"
  },
})
```

### Rule (`rule/<name>.md`)
```yaml
---
description: Rule description
---
Rule instructions applied to agents referencing this rule.
```

### Workspace Template (`workspace-template/<name>.json`)
```json
{
  "name": "template-name",
  "description": "Template description",
  "distro": "ubuntu-noble",
  "skills": ["skill-name"],
  "env_vars": { "KEY": "value" },
  "encrypted_keys": ["SECRET_KEY"],
  "init_scripts": ["base", "ssh-keys"],
  "init_script": "# Custom bash",
  "shared_network": null,
  "tailscale_mode": null,
  "mcps": [],
  "config_profile": "default"
}
```

Note: Sensitive env_vars are automatically encrypted when saved via the API.

### Config Profile (`configs/<profile>/`)
Config profiles contain harness-specific settings:
- `.claudecode/settings.json` - Claude Code settings
- `.opencode/settings.json` - OpenCode settings
- `.ampcode/settings.json` - Amp Code settings
- `.sandboxed-sh/config.json` - Sandboxed.sh settings

See `references/config-editing.md` for details on each config format.

### MCPs (`mcp/servers.json`)
```json
{
  "server-name": {
    "type": "local",
    "command": ["npx", "package-name"],
    "env": { "KEY": "value" },
    "enabled": true
  },
  "remote-server": {
    "type": "remote",
    "url": "https://mcp.example.com",
    "headers": { "Authorization": "Bearer token" },
    "enabled": true
  }
}
```

## Guardrails
- Always read before updating to avoid overwrites
- Keep names lowercase (hyphens allowed) and within 1-64 chars
- Use descriptive commit messages
- Check `library-git_status` before pushing
