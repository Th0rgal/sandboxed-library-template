# Google Gemini / Veo API Notes

Sources: Google AI for Developers docs (Gemini image generation and Veo video).

## Overview (Current Models)

### Image Generation
- `gemini-2.5-flash-image` - Fast, good quality (recommended for most uses)

### Video Generation
- `veo-3.1-generate-preview` - Latest video generation (paid preview)

## Auth and Base URL
- Base URL: `https://generativelanguage.googleapis.com/v1beta`
- Header: `X-goog-api-key: ${GOOGLE_GENAI_API_KEY}`

## Image Generation

Endpoint pattern:
- `POST /models/{model}:generateContent`

### Basic Request
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "X-goog-api-key: ${GOOGLE_GENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "A futuristic cityscape at sunset"}]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "imageSize": "4K",
        "aspectRatio": "16:9"
      }
    }
  }'
```

### Parameters
- `imageSize` values: `"1K"`, `"2K"`, `"4K"` (uppercase K)
- `aspectRatio` values: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9`

### Response
```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "mimeType": "image/jpeg",
          "data": "<base64>"
        }
      }]
    }
  }]
}
```

## Transparency Note

**Gemini does NOT support native transparency output.**

For transparent images, use one of these approaches:
1. **GPT Image 1.5** with `background: "transparent"` (recommended)
2. Generate with Gemini, then use a background removal tool
3. For 3D renders only: use the three-background extraction workflow

The "generate variants on different backgrounds" approach does NOT work reliably with Gemini because each generation produces different results.

## Video Generation (Veo 3.1)

Uses long-running operations for video generation.

### Python SDK Pattern
```python
from google import genai

client = genai.Client(api_key="${GOOGLE_GENAI_API_KEY}")

# Start generation
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A time-lapse of clouds over mountains"
)

# Poll until done
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation.name)

# Download result
video_data = operation.result.generated_videos[0].video
```

### REST Pattern
1. `POST /models/veo-3.1-generate-preview:predictLongRunning`
2. Poll `GET /{operation_name}` until `done=true`
3. Download from `response.generateVideoResponse.generatedSamples[0].video.uri`

### Image-to-Video
Pass a starting image along with the prompt to create video from a still image.

## Rate Limits
- Check current quotas in Google AI Studio
- Video generation has stricter limits than image generation

## Security
- Never store API keys in code
- Use `${GOOGLE_GENAI_API_KEY}` placeholder (substituted during skill sync)
