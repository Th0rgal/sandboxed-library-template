# FFmpeg Codecs Reference

This document provides detailed information about video and audio codecs available in ffmpeg.

## Video Codecs

### H.264 (libx264) - Most Compatible

The most widely supported video codec. Works on virtually all devices and platforms.

```bash
# Basic encoding
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# High quality
ffmpeg -i input.mp4 -c:v libx264 -crf 18 -preset slow output.mp4

# Fast encoding
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset fast output.mp4

# Web compatible (baseline profile)
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p output.mp4

# High profile for best quality
ffmpeg -i input.mp4 -c:v libx264 -profile:v high -level 4.1 output.mp4
```

**Presets** (speed vs compression):
- `ultrafast` - Fastest encoding, largest file
- `superfast`
- `veryfast`
- `faster`
- `fast`
- `medium` - Default
- `slow`
- `slower`
- `veryslow` - Best compression, slowest

**CRF Values** (quality):
- 0 = Lossless
- 18 = Visually lossless
- 23 = Default
- 28 = Smaller file
- 51 = Worst quality

**Profiles**:
- `baseline` - Most compatible, no B-frames
- `main` - Good balance
- `high` - Best quality

### H.265/HEVC (libx265) - Better Compression

50% smaller files than H.264 at same quality. Requires more processing power.

```bash
# Basic encoding
ffmpeg -i input.mp4 -c:v libx265 -crf 28 output.mp4

# High quality
ffmpeg -i input.mp4 -c:v libx265 -crf 22 -preset slow output.mp4

# 10-bit encoding (HDR support)
ffmpeg -i input.mp4 -c:v libx265 -crf 22 -pix_fmt yuv420p10le output.mp4
```

**Note**: CRF values differ from x264. Add ~6 to get equivalent quality (x264 CRF 23 ≈ x265 CRF 28).

### VP9 (libvpx-vp9) - WebM Format

Open source codec used by YouTube. Good for web streaming.

```bash
# Basic encoding
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 output.webm

# Two-pass encoding (recommended)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 2M -pass 1 -an -f null /dev/null && \
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 2M -pass 2 -c:a libopus output.webm

# High quality
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 20 -b:v 0 -deadline good -cpu-used 2 output.webm
```

### AV1 (libaom-av1, libsvtav1) - Best Compression

Newest codec with best compression. Slow to encode.

```bash
# Using libaom-av1 (slow but high quality)
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -cpu-used 4 output.mp4

# Using SVT-AV1 (faster)
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 30 -preset 6 output.mp4

# Using rav1e
ffmpeg -i input.mp4 -c:v librav1e -crf 30 output.mp4
```

### ProRes (prores_ks) - Professional Editing

Lossless/near-lossless codec for editing. Large files.

```bash
# ProRes 422 (standard)
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 2 output.mov

# ProRes 422 HQ (high quality)
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 output.mov

# ProRes 4444 (with alpha channel)
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le output.mov
```

**Profiles**:
- 0 = ProRes 422 Proxy
- 1 = ProRes 422 LT
- 2 = ProRes 422
- 3 = ProRes 422 HQ
- 4 = ProRes 4444
- 5 = ProRes 4444 XQ

### DNxHD/DNxHR - Avid Professional

```bash
# DNxHD for 1080p
ffmpeg -i input.mp4 -c:v dnxhd -profile:v dnxhr_hq output.mov

# DNxHR for higher resolutions
ffmpeg -i input.mp4 -c:v dnxhd -profile:v dnxhr_hqx output.mov
```

### Hardware Accelerated Encoding

#### macOS VideoToolbox (H.264/HEVC)
```bash
# H.264
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# HEVC
ffmpeg -i input.mp4 -c:v hevc_videotoolbox -b:v 5M output.mp4
```

#### NVIDIA NVENC
```bash
# H.264
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 output.mp4

# HEVC
ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p4 -cq 28 output.mp4
```

#### Intel QuickSync
```bash
# H.264
ffmpeg -i input.mp4 -c:v h264_qsv -global_quality 23 output.mp4

# HEVC
ffmpeg -i input.mp4 -c:v hevc_qsv -global_quality 28 output.mp4
```

## Audio Codecs

### AAC - Most Compatible

```bash
# Default AAC
ffmpeg -i input.mp4 -c:a aac -b:a 128k output.mp4

# High quality
ffmpeg -i input.mp4 -c:a aac -b:a 256k output.mp4

# Variable bitrate
ffmpeg -i input.mp4 -c:a aac -q:a 2 output.mp4
```

### MP3 (libmp3lame)

```bash
# Constant bitrate
ffmpeg -i input.wav -c:a libmp3lame -b:a 320k output.mp3

# Variable bitrate (quality 0-9, lower is better)
ffmpeg -i input.wav -c:a libmp3lame -q:a 2 output.mp3
```

**VBR Quality**:
- 0 = ~245 kbps
- 2 = ~190 kbps
- 4 = ~165 kbps
- 6 = ~130 kbps

### Opus (libopus) - Best Quality

Modern codec, best quality at low bitrates.

```bash
# VoIP quality
ffmpeg -i input.wav -c:a libopus -b:a 64k output.opus

# Music quality
ffmpeg -i input.wav -c:a libopus -b:a 128k output.opus

# High quality
ffmpeg -i input.wav -c:a libopus -b:a 256k output.opus
```

### Vorbis (libvorbis) - OGG Format

```bash
ffmpeg -i input.wav -c:a libvorbis -q:a 5 output.ogg
```

### FLAC - Lossless

```bash
# Standard compression
ffmpeg -i input.wav -c:a flac output.flac

# Maximum compression
ffmpeg -i input.wav -c:a flac -compression_level 12 output.flac
```

### WAV/PCM - Uncompressed

```bash
# 16-bit PCM
ffmpeg -i input.mp3 -c:a pcm_s16le output.wav

# 24-bit PCM
ffmpeg -i input.mp3 -c:a pcm_s24le output.wav

# 32-bit float
ffmpeg -i input.mp3 -c:a pcm_f32le output.wav
```

## Container Formats

### MP4 (.mp4)
- Video: H.264, H.265, AV1
- Audio: AAC, MP3, AC3
- Most compatible format

```bash
# Enable fast start for streaming
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

### MKV (.mkv)
- Supports almost all codecs
- Great for archiving
- Less device compatibility

### WebM (.webm)
- Video: VP8, VP9, AV1
- Audio: Vorbis, Opus
- Web-optimized

### MOV (.mov)
- Apple's container format
- Video: H.264, ProRes, HEVC
- Audio: AAC, ALAC

### AVI (.avi)
- Legacy format
- Limited codec support
- Not recommended for new content

## Codec Comparison Table

| Codec | Quality | File Size | Encode Speed | Compatibility |
|-------|---------|-----------|--------------|---------------|
| H.264 | Good | Medium | Fast | Excellent |
| H.265 | Better | Small | Slow | Good |
| VP9 | Better | Small | Slow | Web only |
| AV1 | Best | Smallest | Very slow | Growing |
| ProRes | Excellent | Very large | Fast | Apple/Pro |

## Choosing the Right Codec

### For Social Media/Web
```bash
# H.264 with fast start (most compatible)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k -movflags +faststart output.mp4
```

### For Archiving
```bash
# H.265 for smaller files
ffmpeg -i input.mp4 -c:v libx265 -crf 22 -preset slow -c:a flac output.mkv
```

### For Editing/Post-Production
```bash
# ProRes for quality
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le output.mov
```

### For Streaming
```bash
# HLS with multiple bitrates
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -f hls -hls_time 10 -hls_list_size 0 output.m3u8
```

### For Smallest File Size
```bash
# AV1 (if time permits)
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 35 -preset 4 -c:a libopus -b:a 96k output.mp4
```
