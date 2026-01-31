---
name: skill-creator
description: >
  Guide for creating effective skills. This skill should be used when users
  want to create a new skill (or update an existing skill) that extends
  Claude's capabilities with specialized knowledge, workflows, or tool
  integrations. Trigger terms: create skill, new skill, skill creation,
  update skill, skill template, SKILL.md, skill design.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields Claude reads to determine when the skill gets used.
- **Body** (Markdown): Instructions and guidance. Only loaded AFTER the skill triggers.

#### Bundled Resources (optional)

- **Scripts** (`scripts/`): Executable code for tasks requiring deterministic reliability or repeatedly rewritten code.
- **References** (`references/`): Documentation loaded as needed into context. Keeps SKILL.md lean. For files >10k words, include grep search patterns in SKILL.md.
- **Assets** (`assets/`): Files not loaded into context but used in output (templates, images, fonts, etc.).

#### What to Not Include

Do NOT create extraneous documentation: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, etc. Only include information needed for an AI agent to do the job.

### Progressive Disclosure Design Principle

Skills use a three-level loading system:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (unlimited)

Keep SKILL.md body under 500 lines. Split content into separate files when approaching this limit, and reference them clearly from SKILL.md.

**Key principle:** When a skill supports multiple variations, keep only core workflow and selection guidance in SKILL.md. Move variant-specific details into reference files.

**Important guidelines:**
- **Avoid deeply nested references** - Keep references one level deep from SKILL.md
- **Structure longer reference files** - For files >100 lines, include a table of contents

## Skill Creation Process

Skill creation involves 6 steps. For detailed guidance on each step, see [references/creation-process.md](references/creation-process.md).

1. **Understand** the skill with concrete examples
2. **Plan** reusable skill contents (scripts, references, assets)
3. **Initialize** the skill (run `scripts/init_skill.py <skill-name> --path <output-directory>`)
4. **Edit** the skill (implement resources and write SKILL.md)
5. **Package** the skill (run `scripts/package_skill.py <path/to/skill-folder>`)
6. **Iterate** based on real usage
