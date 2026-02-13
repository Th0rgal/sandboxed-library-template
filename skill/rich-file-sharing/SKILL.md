---
name: rich-file-sharing
description: "Share files and images inline using <image> and <file> component syntax for rich previews in the UI."
---

# Rich File Sharing

Share files and images with rich inline previews using component tags.

## Use when
- You need to present images or downloadable files inline in the UI.
- You want rich previews for artifacts or reports.

## Don't use when
- The UI does not support `<image>`/`<file>` tags.
- You only need to paste raw text or code snippets.

## Outputs
- Inline previews (no additional files created).

## Templates or Examples
- Use the tag examples below as templates.

## Image preview

```
<image path="./chart.png" alt="Sales chart" />
```

Renders an inline image thumbnail. Click to expand. Attributes:
- `path` (required) — relative or absolute path to the image file
- `alt` (optional) — description shown as alt text

## File download card

```
<file path="./report.pdf" name="Q4 Report" />
```

Renders a download card with icon, filename, and size. Attributes:
- `path` (required) — relative or absolute path to the file
- `name` (optional) — display name (defaults to filename)

## Rules

1. **Verify the file exists** before referencing it — the UI shows an error for missing files
2. Use **relative paths** from the workspace root (e.g. `./output/chart.png`)
3. Tags must be **self-closing** (`/>`)
4. Place tags on their **own line** for best rendering
5. Use `<image>` for visual content (PNG, JPG, GIF, WebP, SVG)
6. Use `<file>` for downloads (PDF, CSV, ZIP, code files, etc.)

## Examples

After generating a matplotlib chart:
```
<image path="./output/chart.png" alt="Revenue by quarter" />
```

After creating a data export:
```
<file path="./output/data.csv" name="Exported Data" />
```

Multiple outputs:
```
Here are the results:

<image path="./plots/figure1.png" alt="Distribution plot" />

<file path="./results/summary.json" name="Full Results" />
```
