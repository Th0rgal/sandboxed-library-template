# FFmpeg Commands Reference

## Image Conversion

| Source | Target | Command |
|--------|--------|---------|
| PNG | WebP (lossless) | `ffmpeg -i in.png -lossless 1 out.webp` |
| PNG | WebP (quality) | `ffmpeg -i in.png -quality 90 out.webp` |
| JPEG | WebP | `ffmpeg -i in.jpg -quality 85 out.webp` |
| PNG | Optimized PNG | `ffmpeg -i in.png -compression_level 100 out.png` |

## Video Conversion

| Source | Target | Command |
|--------|--------|---------|
| MP4 | WebM (VP9) | `ffmpeg -i in.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus out.webm` |
| MP4 | MP4 (H.264) | `ffmpeg -i in.mp4 -c:v libx264 -crf 20 -preset slow out.mp4` |
| MP4 | MP4 (H.265) | `ffmpeg -i in.mp4 -c:v libx265 -crf 24 -preset medium out.mp4` |
| Any | MP4 (quick) | `ffmpeg -i in.mov -c:v libx264 -crf 23 -preset fast out.mp4` |

## Batch Processing

### All PNGs to WebP
```bash
for f in *.png; do ffmpeg -i "$f" -quality 90 "${f%.png}.webp"; done
```

### All JPEGs to WebP
```bash
for f in *.jpg; do ffmpeg -i "$f" -quality 85 "${f%.jpg}.webp"; done
```

### All MP4s to WebM
```bash
for f in *.mp4; do ffmpeg -i "$f" -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus -b:a 128k "${f%.mp4}.webm"; done
```

## Useful Options

### Video Presets (-preset)
- `ultrafast` - Fastest, largest file
- `fast` - Good balance for quick jobs
- `medium` - Default
- `slow` - Better compression, slower
- `veryslow` - Best compression, very slow

### Audio Codecs
- `-c:a aac -b:a 128k` - AAC for MP4 containers
- `-c:a libopus -b:a 128k` - Opus for WebM containers
- `-c:a copy` - Copy audio without re-encoding
- `-an` - Remove audio entirely

### Video Filters
```bash
# Scale to 1080p (maintain aspect ratio)
ffmpeg -i in.mp4 -vf "scale=-1:1080" out.mp4

# Scale to 720p
ffmpeg -i in.mp4 -vf "scale=-1:720" out.mp4
```
