# OpenAI GPT Image API (Latest)

Sources: OpenAI API reference for Images and GPT Image 1.5 (Jan 1, 2026). Credentials redacted.

## Latest Model
- `gpt-image-1.5` is the current GPT Image model and is supported by the Images API for generations.

## Which API to Use
- **Images API** supports GPT Image models (`gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`) for **Generations**.
- **Images API Edits** only supports `gpt-image-1` and `dall-e-2` (not `gpt-image-1.5`).

## Auth and Base URL
- Base URL: `https://api.openai.com/v1`
- Header: `Authorization: Bearer ${OPENAI_API_KEY}` (placeholder; replaced at deploy time)

## Image API: Generate
Endpoint:
- `POST https://api.openai.com/v1/images/generations`

Request shape:
```json
{
  "model": "gpt-image-1.5",
  "prompt": "<text prompt>",
  "n": 1,
  "size": "1024x1024",
  "quality": "high",
  "background": "transparent"
}
```

Output:
- GPT image models return base64 image data in `data[0].b64_json`.

Notes:
- `size` for GPT image models supports `1024x1024`, `1536x1024`, `1024x1536`, or `auto`.
- `quality` supports `low`, `medium`, `high`, or `auto` for GPT image models.
- `background` can be `transparent`, `opaque`, or `auto` (transparent requires `png` or `webp`).
- `output_format` supports `png`, `jpeg`, `webp` for GPT image models; GPT image models always return base64 (not URLs).
- `n` can be 1-10 for GPT image models.

## Image API: Edit (Inpainting / Variants)
Endpoint:
- `POST https://api.openai.com/v1/images/edits`

Typical multipart fields:
- `model=gpt-image-1`
- `image[]=@input.png` (one or more images)
- `mask=@mask.png` (optional; defines the area to replace)
- `prompt=...`

Edits endpoint accepts image inputs and optional masks; response returns base64 output.

Notes:
- For GPT image models, each input image must be `png`, `webp`, or `jpg` and under 50MB; up to 16 images.

## Responses API (Image Generation Tool)
- Use a mainline model that supports the `image_generation` tool, and it will call a GPT Image model under the hood.

## Security
- Do not store API keys in repo.
- Use environment variables or local config files ignored by Git.
