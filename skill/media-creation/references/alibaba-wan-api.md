# Alibaba Wan 2.6 (DashScope) API Notes

Sources: Alibaba Cloud DashScope API references for Wan 2.6 text-to-video, image-to-video, and image generation. Credentials redacted.

## Overview (latest models only)
- Text-to-video: `wan2.6-t2v`
- Image-to-video: `wan2.6-i2v`
- Image generation / editing: `wan2.6-image`

## Auth and Base URL
- Base URL (Singapore): `https://dashscope-intl.aliyuncs.com/api/v1`
- Header: `Authorization: Bearer ${DASHSCOPE_API_KEY}` (placeholder; replaced at deploy time)
- Async header (for task-based flows): `X-DashScope-Async: enable`

## Video Generation (Wan 2.6)

Endpoint:
- `POST /services/aigc/video-generation/video-synthesis`

Text-to-video (T2V) request shape:
```json
{
  "model": "wan2.6-t2v",
  "input": {
    "prompt": "<scene and motion prompt>",
    "audio_url": "<optional audio URL>"
  },
  "parameters": {
    "size": "1280*720",
    "duration": 5,
    "prompt_extend": true
  }
}
```

Image-to-video (I2V) request shape:
```json
{
  "model": "wan2.6-i2v",
  "input": {
    "prompt": "<motion prompt>",
    "img_url": "data:image/jpeg;base64,<BASE64>",
    "audio_url": "<optional audio URL>"
  },
  "parameters": {
    "resolution": "1080P",
    "duration": 5,
    "prompt_extend": true,
    "shot_type": "multi"
  }
}
```

Notes:
- T2V uses `size` (e.g., `1280*720`); I2V uses `resolution` (720P/1080P).
- `duration` for Wan 2.6 is 5, 10, or 15 seconds.
- Multi-shot narrative is available via `shot_type: "multi"` when `prompt_extend` is true (Wan 2.6).

Task flow:
- Response returns `output.task_id` and `output.task_status`.
- Poll `GET /tasks/{task_id}` until `SUCCEEDED`, then use `output.video_url`.

## Image Generation (Wan 2.6)

Two HTTP options are documented:
1) **Sync/SSE**: `POST /services/aigc/multimodal-generation/generation`
2) **Async**: `POST /services/aigc/image-generation/generation` with `X-DashScope-Async: enable`

Request shape:
```json
{
  "model": "wan2.6-image",
  "input": {
    "messages": [
      {"role": "user", "content": [
        {"text": "<image prompt>"},
        {"image": "<optional URL or base64 data URI>"}
      ]}
    ]
  },
  "parameters": {
    "size": "1024*1024",
    "n": 1,
    "prompt_extend": true,
    "watermark": false
  }
}
```

Async response returns a task ID; poll `GET /tasks/{task_id}` for result URLs.

## Input Requirements (image fields)
- `image` or `img_url` can be a public URL or base64 data URI
- Data URI format: `data:{MIME_type};base64,{base64_data}`

## Security
- Do not store API keys in repo.
- Use environment variables or a local config file ignored by Git.
