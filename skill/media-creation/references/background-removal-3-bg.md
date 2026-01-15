# Background Removal (Three-Background Method)

Script location: `scripts/extract_transparency.py`

## When to Use This Method

**This workflow is ONLY suitable for:**
- 3D renders (Blender, Maya, Cinema 4D, etc.)
- Compositing software (After Effects, Nuke, Fusion)
- Screenshots with controlled desktop backgrounds
- Any situation where you can render the EXACT same pixels on different backgrounds

**This workflow does NOT work for:**
- AI-generated images (Gemini, DALL-E, Midjourney, etc.)
- Photos that need background removal
- Any source where the foreground changes between captures

For AI-generated transparent images, use **GPT Image 1.5** with `background: "transparent"` instead.

## Why It Doesn't Work with Generative AI

The algorithm relies on this equation for each pixel:
```
Result = ForegroundColor × Alpha + BackgroundColor × (1 - Alpha)
```

This only works when `ForegroundColor` and `Alpha` are IDENTICAL across all three images. Generative AI models produce different outputs each time, even with the same prompt.

## Problem Setup

Given three renders of the same image:
- Black background (B=0)
- White background (B=1)
- Colored background (default red: B=(1,0,0))

For a pixel with true color C and alpha A composited over background B:
```
Result = C × A + B × (1 - A)
```

## Algorithm

### Two-Background Alpha (Black + White)
From black and white backgrounds:
- Black: `R_black = C × A`
- White: `R_white = C × A + (1 - A)`

Solve for alpha (per channel):
```
A = 1 - (R_white - R_black)
```

Implementation:
- Compute alpha per channel, then average across RGB
- Clamp alpha to [0, 1]

### Three-Background Refinement
The third (colored) background improves accuracy:

For a colored background channel where component > 0.1:
```
A = 1 - (R_colored - R_black) / B
```

Weighted average:
- 50% weight to black/white estimate
- 50% distributed across colored-channel estimates

### Color Recovery
Color is recovered from the black background:
```
C = R_black / A  (with epsilon to avoid divide-by-zero)
```

If A is effectively zero, color is set to 0.

## Usage

```bash
# Full three-background extraction (best quality)
python3 scripts/extract_transparency.py \
  --black render_black.png \
  --white render_white.png \
  --colored render_red.png \
  --output result.png

# Two-background extraction (simpler, still good)
python3 scripts/extract_transparency.py \
  --black render_black.png \
  --white render_white.png \
  --output result.png

# Custom colored background (e.g., green)
python3 scripts/extract_transparency.py \
  --black render_black.png \
  --white render_white.png \
  --colored render_green.png \
  --colored-rgb 0.0 1.0 0.0 \
  --output result.png
```

## Output
- Combines RGB color and alpha into an RGBA PNG
- Creates a `_preview.png` with checkerboard background for visualization
- Prints alpha statistics (min, max, transparent/opaque pixel counts)

## Two-Background Option (Quality Tradeoff)

Using only black + white gives good results. Using black + colored (without white) is weaker:
- Colored background only provides alpha for its non-zero channels
- Example: red background gives no new information for green/blue channels

**Recommendation**: Use black + white if limited to two images; use all three for best accuracy.

## Technical Notes
- Images must have identical dimensions
- All inputs are normalized to [0, 1] float32
- Colored background defaults to red `(1.0, 0.0, 0.0)`
- Output is saved as PNG with full transparency support
