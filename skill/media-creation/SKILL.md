---
name: media-creation
description: >
  Creates images and video via Alibaba Wan 2.6 (DashScope), Google Gemini/Veo, and OpenAI GPT Image 1.5 APIs, plus background extraction workflows.
  Trigger terms: image generation, video generation, dashscope, wan 2.6, alibaba, gemini, veo, gpt image, openai images, background removal, alpha extraction, transparent png.
---

## Use when
- Generate images or video via Alibaba Wan, Google Gemini/Veo, or OpenAI GPT Image APIs.
- Create transparent PNGs (prefer GPT Image 1.5 for native transparency support).
- Convert consistent renders (3D, compositing) with different backgrounds into a transparent RGBA output.
- Prefer Gemini for general image generation; use Wan when content is restricted (e.g., babies).

## Don't use when
- If API access or credentials are not available.
- If the task does not involve media generation or background extraction.

## Outputs
- Generated media files in `artifacts/` (PNG, WEBP, MP4, etc.) or API JSON responses when requested.

## Templates or Examples
- Use the API request examples below as templates.

## Transparent Image Generation (Recommended Approach)

### Option 1: GPT Image 1.5 Native Transparency (BEST)
GPT Image 1.5 supports native transparency output. This is the simplest and most reliable method:

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
- This is the only method that produces TRUE transparency from a single generation

### Option 2: Three-Background Extraction (For Consistent Renders Only)
**⚠️ IMPORTANT LIMITATION**: This workflow ONLY works when you have control over the exact pixel output:
- ✅ 3D renders (Blender, Maya, etc.)
- ✅ Compositing software with controlled backgrounds
- ✅ Screenshots with different desktop backgrounds
- ❌ Generative AI (each generation produces different results)

The algorithm requires IDENTICAL foreground pixels across all three images. Generative AI models produce different outputs even with the same prompt.

For 3D/compositing use:
```bash
python3 scripts/extract_transparency.py \
  --black render_black.png \
  --white render_white.png \
  --colored render_red.png \
  --output result.png
```

### Option 3: AI Image + Manual Background Removal
For AI-generated images that need transparency:
1. Generate the image with any provider
2. Use a dedicated background removal tool (rembg, remove.bg API, etc.)

## Inputs the Agent Should Ask For (only if missing; otherwise proceed)
- Provider: Alibaba Wan (DashScope), Google (Gemini/Veo), or OpenAI (GPT Image).
- Model ID and task type (T2I, I2V, T2V).
- Prompt text and any input image path (for I2V).
- Output size/resolution and aspect ratio.
- Desired output format and count.
- For transparency: whether native transparency (GPT Image) or background extraction is needed.
- For background extraction: paths to black/white/red background images and the colored background RGB (0-1).

## API Keys
The following environment variables should be set for API access:
- `OPENAI_API_KEY` - For GPT Image 1.5 generations
- `GOOGLE_GENAI_API_KEY` - For Gemini image/Veo video generation
- `DASHSCOPE_API_KEY` - For Alibaba Wan 2.6 image/video generation

## Outputs / Definition of Done
- A clear, credential-safe request plan or script snippet.
- For generation: task submission, polling, and decode/download steps.
- For background removal: algorithm steps and expected RGBA output.

## Procedure
- Use `references/alibaba-wan-api.md` for Wan 2.6 endpoints and parameters (image, T2V, I2V).
- Use `references/gemini-banana-api.md` for Gemini image and Veo video in the Gemini API.
- Use `references/openai-gpt-image-api.md` for GPT Image 1.5 endpoints and parameters.
- Use `references/background-removal-3-bg.md` for the three-background alpha extraction algorithm.
- API keys in code examples are stored encrypted using `<encrypted>` tags.

## Model Quick Reference

| Provider | Model | Use Case |
|----------|-------|----------|
| OpenAI | `gpt-image-1.5` | Best for transparent images, high quality |
| OpenAI | `gpt-image-1` | Image edits/inpainting |
| Google | `gemini-2.5-flash-image` | Fast image generation |
| Google | `veo-3.1-generate-preview` | Video generation |
| Alibaba | `wan2.6-t2v` | Text-to-video |
| Alibaba | `wan2.6-i2v` | Image-to-video |
| Alibaba | `wan2.6-image` | Image generation (fewer restrictions) |

## Checks & Guardrails
- API keys must be wrapped in `<encrypted>` tags; they are encrypted at rest.
- Validate image sizes/formats and rate limits.
- Ensure base64 encoding formats match API expectations.
- For transparency: verify the workflow matches the source type (render vs. AI).

## References
- references/alibaba-wan-api.md
- references/gemini-banana-api.md
- references/openai-gpt-image-api.md
- references/background-removal-3-bg.md

## Scripts
- `scripts/extract_transparency.py` - Extract RGBA from black/white/red background images.
  Usage: `python3 scripts/extract_transparency.py --black img_black.png --white img_white.png --colored img_red.png --output result.png`
