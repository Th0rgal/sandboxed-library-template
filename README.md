# OpenAgent Library Template

This is the default template for OpenAgent configuration libraries. Fork this repository to create your own library with custom skills, commands, tools, rules, and agents.

## Structure

```
library/
├── skill/              # Reusable skills (SKILL.md + reference files)
├── command/            # Slash commands (markdown with YAML frontmatter)
├── tool/               # Custom TypeScript tools (@opencode-ai/plugin)
├── rule/               # Reusable instruction sets
├── agent/              # Custom agent configurations
├── mcp/                # MCP server configurations (servers.json)
├── opencode/           # OpenCode plugin configs (oh-my-opencode.json)
└── workspace-template/ # Workspace templates (distro/skills/env/init script)
```

## Built-in Library Tools

This template includes tools for managing library content programmatically:

### `library-skills.ts`
- `list_skills` - List all skills in the library
- `get_skill` - Get full skill content by name
- `save_skill` - Create or update a skill
- `delete_skill` - Delete a skill

### `library-commands.ts`
- `list_commands` - List all slash commands
- `get_command` - Get command content
- `save_command` - Create or update a command
- `delete_command` - Delete a command
- `list_tools` - List custom tools
- `get_tool` - Get tool source code
- `save_tool` - Create or update a tool
- `delete_tool` - Delete a tool
- `list_rules` - List rules
- `get_rule` - Get rule content
- `save_rule` - Create or update a rule
- `delete_rule` - Delete a rule

### `library-git.ts`
- `status` - Get library git status
- `sync` - Pull latest changes from remote
- `commit` - Commit changes with a message
- `push` - Push to remote
- `get_mcps` - Get MCP server configurations
- `save_mcps` - Save MCP configurations

## Usage

1. Fork this repository
2. Configure your OpenAgent instance with `LIBRARY_REMOTE=git@github.com:your-username/your-library.git`
3. Add skills, commands, and tools via the dashboard or using the library tools

## Creating Skills

Skills are directories containing a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: Description of what this skill does
---

Instructions for the agent on how to use this skill...
```

## Creating Commands

Commands are markdown files with YAML frontmatter:

```markdown
---
description: What this command does
model: claude-sonnet-4-20250514
---

Prompt template for the command...
```

## Creating Tools

Tools are TypeScript files using `@opencode-ai/plugin`:

```typescript
import { tool } from "@opencode-ai/plugin"

export const my_tool = tool({
  description: "What this tool does",
  args: {
    param: tool.schema.string().describe("Parameter description"),
  },
  async execute(args) {
    // Tool implementation
    return "Result"
  },
})
```
