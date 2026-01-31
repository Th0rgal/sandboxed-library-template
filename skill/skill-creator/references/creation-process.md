# Skill Creation Process (Detailed)

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

## Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

## Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

## Step 3: Initializing the Skill

Skip this step if the skill already exists and only iteration or packaging is needed.

When creating a new skill from scratch, always run the `init_skill.py` script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

## Step 4: Edit the Skill

When editing the skill, remember that the skill is being created for another instance of Claude to use. Include information that would be beneficial and non-obvious to Claude.

### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See references/workflows.md for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See references/output-patterns.md for template and example patterns

### Start with Reusable Skill Contents

Begin implementation with the reusable resources identified in Step 2. Note that this step may require user input (e.g., brand assets, templates, documentation).

Added scripts must be tested by actually running them. Any example files not needed should be deleted.

### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

#### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: Primary triggering mechanism. Include both what the Skill does and specific triggers/contexts for when to use it. Include all "when to use" information here - not in the body.

Do not include any other fields in YAML frontmatter.

#### Body

Write instructions for using the skill and its bundled resources.

## Step 5: Packaging a Skill

Package the skill into a distributable .skill file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory: `scripts/package_skill.py <path/to/skill-folder> ./dist`

The script validates then packages. Fix validation errors and re-run if needed.

## Step 6: Iterate

After testing, iterate based on real usage:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
