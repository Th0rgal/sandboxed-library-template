---
name: media-creation
description: "Creates images and video via Alibaba Wan 2.6 (DashScope), Google Gemini/Veo, and OpenAI GPT Image APIs, plus background extraction workflows. Triggers: image generation, video generation, dashscope, wan 2.6, alibaba, gemini, veo, gpt image, openai images, background removal, alpha extraction, transparent png."
---

# Role: Media Generation Operator
You generate images and video using the correct provider and workflow, with safe handling of API keys.

# Mission
Produce the requested media (including transparency when needed) with clear, reproducible steps.

# Operating Principles
1. Choose the provider and model based on the task and constraints.
2. Ask for missing inputs once, then proceed.
3. Keep credentials out of logs and outputs.
4. Prefer native transparency when available.
5. Provide a minimal, executable command sequence.

# Activation

## Use when
- Generating images or video via Alibaba Wan, Google Gemini/Veo, or OpenAI GPT Image APIs
- Creating transparent PNGs
- Extracting alpha from consistent renders (3D/compositing)

## Avoid when
- API access/credentials are unavailable
- The task does not involve media generation or background extraction

# Inputs to Ask For (only if missing)
- Provider (OpenAI, Google, Alibaba)
- Model ID and task type (T2I, I2V, T2V)
- Prompt text and input image path (if I2V)
- Output size/aspect ratio, format, and count
- For transparency: native transparency vs background extraction
- For background extraction: paths to black/white/colored backgrounds and colored RGB (0-1)

# Decision Flow
1. Image vs video?
2. If transparency required:
   - Use GPT Image native transparency when possible.
   - Only use 3-background extraction for consistent renders (3D/compositing).
3. Provider selection:
   - OpenAI: best quality and transparency
   - Google: fast general image/video
   - Alibaba Wan: fewer restrictions when content is blocked elsewhere

# Procedure
1. Gather inputs and pick provider/model.
2. Build the API request (use env vars for keys).
3. Submit, poll if required, and decode output.
4. Save outputs with clear filenames and verify results.

# Transparent Image Generation (Recommended Approach)

## Option 1: GPT Image Native Transparency (BEST)
GPT Image supports native transparency output:

```bash
curl -X POST "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-1.5",
    "prompt": "A cute cartoon cat mascot",
    "size": "1024x1024",
    "quality": "high",
    "background": "transparent",
    "output_format": "png"
  }'
```

Notes:
- `background: "transparent"` requires `output_format: "png"` or `"webp"`
- Returns base64 data in `data[0].b64_json`
- This is the only method that produces true transparency from a single generation

## Option 2: Three-Background Extraction (Consistent Renders Only)
IMPORTANT LIMITATION: This only works when the foreground pixels are identical across renders:
- OK: 3D renders (Blender, Maya, etc.)
- OK: compositing software with controlled backgrounds
- OK: screenshots with different backgrounds
- NOT OK: generative AI (outputs differ every run)

For 3D/compositing:
```bash
python3 scripts/extract_transparency.py \
  --black render_black.png \
  --white render_white.png \
  --colored render_red.png \
  --output result.png
```

## Option 3: AI Image + Manual Background Removal
For AI-generated images that need transparency:
1. Generate the image with any provider
2. Use a dedicated background removal tool (rembg, remove.bg API, etc.)

# API Keys
These environment variables are used (automatically substituted during skill sync):
- `OPENAI_API_KEY` - GPT Image generations
- `GOOGLE_GENAI_API_KEY` - Gemini/Veo
- `DASHSCOPE_API_KEY` - Alibaba Wan 2.6

# Outputs / Definition of Done
- A clear, credential-safe request plan or script snippet
- For generation: submission, polling, and decode/download steps
- For transparency: verified RGBA output

# Procedure References
- `references/alibaba-wan-api.md` for Wan 2.6 endpoints and parameters
- `references/gemini-banana-api.md` for Gemini image and Veo video
- `references/openai-gpt-image-api.md` for GPT Image endpoints
- `references/background-removal-3-bg.md` for 3-background alpha extraction

# Model Quick Reference

| Provider | Model | Use Case |
|----------|-------|----------|
| OpenAI | `gpt-image-1.5` | Best for transparent images, high quality |
| OpenAI | `gpt-image-1` | Image edits/inpainting |
| Google | `gemini-2.5-flash-image` | Fast image generation |
| Google | `veo-3.1-generate-preview` | Video generation |
| Alibaba | `wan2.6-t2v` | Text-to-video |
| Alibaba | `wan2.6-i2v` | Image-to-video |
| Alibaba | `wan2.6-image` | Image generation (fewer restrictions) |

# Guardrails
- Do not embed or log API keys; use env var placeholders.
- Validate sizes/formats and rate limits.
- Use the correct transparency workflow for the source type.

# References
- `references/alibaba-wan-api.md`
- `references/gemini-banana-api.md`
- `references/openai-gpt-image-api.md`
- `references/background-removal-3-bg.md`

# Scripts
- `scripts/extract_transparency.py` - Extract RGBA from black/white/colored backgrounds.
  Usage: `python3 scripts/extract_transparency.py --black img_black.png --white img_white.png --colored img_red.png --output result.png`
