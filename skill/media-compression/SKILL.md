---
name: media-compression
description: >
  Compress images and videos using FFmpeg for storage efficiency without quality loss.
  Trigger terms: compress, compression, ffmpeg, convert, webp, webm, optimize,
  reduce file size, smaller, image compression, video compression, mp4, png, jpeg.
---

## When to Use
- Converting images to WebP for smaller file sizes
- Converting videos to WebM (VP9) for better web delivery
- Optimizing MP4 files with H.264/H.265
- Batch processing media files for storage savings
- Reducing file sizes before upload or deployment

## When NOT to Use
- Audio-only processing (use dedicated audio tools)
- Streaming/live video encoding
- Professional video editing (use Premiere, DaVinci)
- When lossless quality is absolutely required and file size doesn't matter

## Inputs the Agent Should Ask For (only if missing)
- **Source file(s)**: Path to image(s) or video(s) to compress
- **Target format** (optional): WebP, WebM, or optimized MP4
- **Quality preference**: "visually lossless" (default) or "maximum compression"

## Outputs / Definition of Done
- Compressed file(s) in target format
- Size comparison: original vs compressed
- Quality verification (visual check or metrics)

## Procedure

### 1. Check FFmpeg Installation
```bash
ffmpeg -version
```
If not installed: `brew install ffmpeg` (macOS)

### 2. Image Compression

**PNG/JPEG to WebP (recommended):**
```bash
# Near-lossless (visually identical, ~50-70% smaller)
ffmpeg -i input.png -quality 90 output.webp
ffmpeg -i input.jpg -quality 85 output.webp

# Lossless (identical quality, ~25-35% smaller)
ffmpeg -i input.png -lossless 1 output.webp
```

**Batch convert:**
```bash
for f in *.png; do ffmpeg -i "$f" -quality 90 "${f%.png}.webp"; done
```

### 3. Video Compression

**MP4 to WebM (VP9):**
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus -b:a 128k output.webm
```

**Optimize MP4 (H.264):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 20 -preset slow -c:a aac -b:a 128k output.mp4
```

**MP4 with H.265 (best compression):**
```bash
ffmpeg -i input.mp4 -c:v libx265 -crf 24 -preset medium -c:a aac -b:a 128k output.mp4
```

### 4. Report Results
Show before/after file sizes:
```bash
ls -lh input.* output.*
```

## Checks & Guardrails
- Always keep original files until compression is verified
- Preview a short clip before batch processing videos
- Use CRF values in recommended ranges (see references)
- H.265 requires compatible players; H.264 has wider support

## References
- [FFmpeg Commands Reference](references/ffmpeg-commands.md)
- [CRF Values Guide](references/crf-guide.md)
