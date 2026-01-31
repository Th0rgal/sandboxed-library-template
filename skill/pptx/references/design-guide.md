# PPTX Design Guide

## Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:
1. **Consider the subject matter**: What is this presentation about? What tone, industry, or mood does it suggest?
2. **Check for branding**: If the user mentions a company/organization, consider their brand colors and identity
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain your design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, and visual language across slides

### Color Palette Selection

**Choosing colors creatively**:
- **Think beyond defaults**: What colors genuinely match this specific topic? Avoid autopilot choices.
- **Consider multiple angles**: Topic, industry, mood, energy level, target audience, brand identity (if mentioned)
- **Be adventurous**: Try unexpected combinations - a healthcare presentation doesn't have to be green, finance doesn't have to be navy
- **Build your palette**: Pick 3-5 colors that work together (dominant colors + supporting tones + accent)
- **Ensure contrast**: Text must be clearly readable on backgrounds

**Example color palettes** (use these to spark creativity - choose one, adapt it, or create your own):

1. **Classic Blue**: Deep navy (#1C2833), slate gray (#2E4053), silver (#AAB7B8), off-white (#F4F6F6)
2. **Teal & Coral**: Teal (#5EA8A7), deep teal (#277884), coral (#FE4447), white (#FFFFFF)
3. **Bold Red**: Red (#C0392B), bright red (#E74C3C), orange (#F39C12), yellow (#F1C40F), green (#2ECC71)
4. **Warm Blush**: Mauve (#A49393), blush (#EED6D3), rose (#E8B4B8), cream (#FAF7F2)
5. **Burgundy Luxury**: Burgundy (#5D1D2E), crimson (#951233), rust (#C15937), gold (#997929)
6. **Deep Purple & Emerald**: Purple (#B165FB), dark blue (#181B24), emerald (#40695B), white (#FFFFFF)
7. **Cream & Forest Green**: Cream (#FFE1C7), forest green (#40695B), white (#FCFCFC)
8. **Pink & Purple**: Pink (#F8275B), coral (#FF574A), rose (#FF737D), purple (#3D2F68)
9. **Lime & Plum**: Lime (#C5DE82), plum (#7C3A5F), coral (#FD8C6E), blue-gray (#98ACB5)
10. **Black & Gold**: Gold (#BF9A4A), black (#000000), cream (#F4F6F6)
11. **Sage & Terracotta**: Sage (#87A96B), terracotta (#E07A5F), cream (#F4F1DE), charcoal (#2C2C2C)
12. **Charcoal & Red**: Charcoal (#292929), red (#E33737), light gray (#CCCBCB)
13. **Vibrant Orange**: Orange (#F96D00), light gray (#F2F2F2), charcoal (#222831)
14. **Forest Green**: Black (#191A19), green (#4E9F3D), dark green (#1E5128), white (#FFFFFF)
15. **Retro Rainbow**: Purple (#722880), pink (#D72D51), orange (#EB5C18), amber (#F08800), gold (#DEB600)
16. **Vintage Earthy**: Mustard (#E3B448), sage (#CBD18F), forest green (#3A6B35), cream (#F4F1DE)
17. **Coastal Rose**: Old rose (#AD7670), beaver (#B49886), eggshell (#F3ECDC), ash gray (#BFD5BE)
18. **Orange & Turquoise**: Light orange (#FC993E), grayish turquoise (#667C6F), white (#FCFCFC)

### Visual Details Options

**Geometric Patterns**:
- Diagonal section dividers instead of horizontal
- Asymmetric column widths (30/70, 40/60, 25/75)
- Rotated text headers at 90° or 270°
- Circular/hexagonal frames for images
- Triangular accent shapes in corners
- Overlapping shapes for depth

**Border & Frame Treatments**:
- Thick single-color borders (10-20pt) on one side only
- Double-line borders with contrasting colors
- Corner brackets instead of full frames
- L-shaped borders (top+left or bottom+right)
- Underline accents beneath headers (3-5pt thick)

**Typography Treatments**:
- Extreme size contrast (72pt headlines vs 11pt body)
- All-caps headers with wide letter spacing
- Numbered sections in oversized display type
- Monospace (Courier New) for data/stats/technical content
- Condensed fonts (Arial Narrow) for dense information
- Outlined text for emphasis

**Chart & Data Styling**:
- Monochrome charts with single accent color for key data
- Horizontal bar charts instead of vertical
- Dot plots instead of bar charts
- Minimal gridlines or none at all
- Data labels directly on elements (no legends)
- Oversized numbers for key metrics

**Layout Innovations**:
- Full-bleed images with text overlays
- Sidebar column (20-30% width) for navigation/context
- Modular grid systems (3×3, 4×4 blocks)
- Z-pattern or F-pattern content flow
- Floating text boxes over colored shapes
- Magazine-style multi-column layouts

**Background Treatments**:
- Solid color blocks occupying 40-60% of slide
- Gradient fills (vertical or diagonal only)
- Split backgrounds (two colors, diagonal or vertical)
- Edge-to-edge color bands
- Negative space as a design element

### Layout Tips

**When creating slides with charts or tables:**
- **Two-column layout (PREFERRED)**: Use a header spanning the full width, then two columns below - text/bullets in one column and the featured content in the other. This provides better balance and makes charts/tables more readable. Use flexbox with unequal column widths (e.g., 40%/60% split) to optimize space for each content type.
- **Full-slide layout**: Let the featured content (chart/table) take up the entire slide for maximum impact and readability
- **NEVER vertically stack**: Do not place charts/tables below text in a single column - this causes poor readability and layout issues

## Template Workflow (Detailed Steps)

When creating a presentation using a template, follow these detailed steps after step 1 (extract template text and thumbnail grid):

### Step 2: Analyze template and save inventory

* **Visual Analysis**: Review thumbnail grid(s) to understand slide layouts, design patterns, and visual structure
* Create and save a template inventory file at `template-inventory.md` containing:
  ```markdown
  # Template Inventory Analysis
  **Total Slides: [count]**
  **IMPORTANT: Slides are 0-indexed (first slide = 0, last slide = count-1)**

  ## [Category Name]
  - Slide 0: [Layout code if available] - Description/purpose
  - Slide 1: [Layout code] - Description/purpose
  [... EVERY slide must be listed individually with its index ...]
  ```
* This inventory file is REQUIRED for selecting appropriate templates in the next step

### Step 3: Create presentation outline

* Review available templates from step 2.
* **CRITICAL: Match layout structure to actual content**:
  - Single-column layouts: Use for unified narrative or single topic
  - Two-column layouts: Use ONLY when you have exactly 2 distinct items/concepts
  - Three-column layouts: Use ONLY when you have exactly 3 distinct items/concepts
  - Image + text layouts: Use ONLY when you have actual images to insert
  - Quote layouts: Use ONLY for actual quotes from people (with attribution), never for emphasis
  - Never use layouts with more placeholders than you have content
* Count your actual content pieces BEFORE selecting the layout
* Save `outline.md` with content AND template mapping:
  ```
  template_mapping = [
      0,   # Use slide 0 (Title/Cover)
      34,  # Use slide 34 (B1: Title and body)
      50,  # Use slide 50 (E1: Quote)
  ]
  ```

### Step 4: Duplicate, reorder, and delete slides

```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
```

Slide indices are 0-based. The same index can appear multiple times to duplicate.

### Step 5: Extract ALL text using inventory.py

```bash
python scripts/inventory.py working.pptx text-inventory.json
```

Read the entire text-inventory.json to understand all shapes and properties.

The inventory JSON structure:
```json
{
  "slide-0": {
    "shape-0": {
      "placeholder_type": "TITLE",
      "left": 1.5, "top": 2.0, "width": 7.5, "height": 1.2,
      "paragraphs": [
        {
          "text": "Paragraph text",
          "bullet": true, "level": 0,
          "alignment": "CENTER",
          "font_name": "Arial", "font_size": 14.0,
          "bold": true, "color": "FF0000"
        }
      ]
    }
  }
}
```

Key features:
- **Slides**: Named as "slide-0", "slide-1", etc.
- **Shapes**: Ordered by visual position as "shape-0", "shape-1", etc.
- **Placeholder types**: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, or null
- **Bullets**: When `bullet: true`, `level` is always included (even if 0)
- **Properties**: Only non-default values are included in the output

### Step 6: Generate replacement text

Based on the text inventory:
- **CRITICAL**: First verify which shapes exist in the inventory
- **AUTOMATIC CLEARING**: ALL text shapes from the inventory will be cleared unless you provide "paragraphs" for them
- **IMPORTANT**: When bullet: true, do NOT include bullet symbols (•, -, *) in text
- **ESSENTIAL FORMATTING RULES**:
  - Headers/titles should typically have `"bold": true`
  - List items should have `"bullet": true, "level": 0`
  - Preserve alignment properties
  - Colors: Use `"color": "FF0000"` for RGB or `"theme_color": "DARK_1"` for theme colors
- Save to `replacement-text.json`

### Step 7: Apply replacements

```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```

## Creating Thumbnail Grids

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

**Features**:
- Creates: `thumbnails.jpg` (or `thumbnails-1.jpg`, `thumbnails-2.jpg`, etc. for large decks)
- Default: 5 columns, max 30 slides per grid (5×6)
- Custom prefix: `python scripts/thumbnail.py template.pptx my-grid`
- Adjust columns: `--cols 4` (range: 3-6)
- Slides are zero-indexed

**Examples**:
```bash
python scripts/thumbnail.py presentation.pptx
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## Converting Slides to Images

1. **Convert PPTX to PDF**: `soffice --headless --convert-to pdf template.pptx`
2. **Convert PDF pages to JPEG**: `pdftoppm -jpeg -r 150 template.pdf slide`

Options: `-r 150` (DPI), `-f N` (first page), `-l N` (last page)
