---
name: ffmpeg
description: Extract audio and transcode MP4 to WebM using ffmpeg.
---

# ffmpeg

## Scope
Use this skill to:
- Extract audio from a video file.
- Transcode an MP4 video to WebM.

## Requirements
- Prefer safe defaults and explicit codecs.
- Keep commands minimal and reproducible.
- Use ASCII-only output unless file already uses Unicode.

## Commands

### Extract audio (MP4 → MP3)
```
ffmpeg -y -i input.mp4 -vn -c:a libmp3lame -q:a 2 output.mp3
```

### Extract audio (MP4 → WAV, lossless)
```
ffmpeg -y -i input.mp4 -vn -c:a pcm_s16le -ar 44100 -ac 2 output.wav
```

### Transcode MP4 → WebM (VP9 + Opus)
```
ffmpeg -y -i input.mp4 -c:v libvpx-vp9 -crf 32 -b:v 0 -row-mt 1 -c:a libopus -b:a 128k output.webm
```

### Transcode MP4 → WebM (VP8 + Vorbis)
```
ffmpeg -y -i input.mp4 -c:v libvpx -crf 10 -b:v 1M -c:a libvorbis -b:a 128k output.webm
```

## Notes
- `-y` overwrites output files. Remove if you want interactive prompts.
- Lower `-crf` means higher quality (and larger files).
- If audio-only extraction is desired, use `-vn` to drop video.
