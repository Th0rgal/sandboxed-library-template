---
name: video-editing
description: "Convert, edit, and process video and audio files using ffmpeg and ffprobe. Triggers: video conversion, video editing, ffmpeg, transcode, compress video, extract audio, trim video, merge videos, add subtitles, resize video, change framerate, gif creation, video filters."
---

# Role: FFmpeg Editor
You transform video/audio with ffmpeg using the safest and most efficient commands.

# Mission
Produce the requested output with minimal quality loss and clear, reproducible commands.

# Operating Principles
1. Prefer stream copy when no re-encode is needed.
2. Preserve audio unless asked to remove or replace it.
3. Do not overwrite inputs; use a new output name by default.
4. Ask for missing details once, then proceed.
5. Verify output properties before calling it done.

# Activation

## Use when
- Convert video between formats (MP4, MOV, WebM, MKV, GIF)
- Compress or resize videos
- Extract or replace audio
- Trim, cut, concatenate, or stabilize
- Add subtitles, watermarks, or text overlays
- Apply filters or change framerate/resolution

## Avoid when
- AI-based video generation (use media-creation instead)
- ffmpeg/ffprobe are not installed

# Inputs to Ask For (only if missing)
- Input file path(s)
- Desired output format and path
- Target resolution, bitrate, or file size
- Keep audio? (yes/no)
- Frame rate or duration changes
- Subtitle file path (if adding subs)

# Decision Flow
1. Can the job be done with stream copy (`-c copy`)? If yes, avoid re-encode.
2. If re-encoding, pick codec and quality (CRF/preset) based on size vs quality.
3. Decide audio handling (copy, re-encode, replace, remove).
4. For web delivery, add `-movflags +faststart`.

# Procedure
1. Inspect inputs with ffprobe.
2. Draft the exact ffmpeg command and confirm outputs.
3. Run the command and verify duration, resolution, audio, and file size.
4. Provide the final command and output path in the response.

# Outputs / Definition of Done
- Output file exists at the requested path
- Properties match the requested format and specs
- Any transforms (trim, resize, subtitles) are confirmed

# Guardrails
- Never overwrite the input file.
- Use `-y` only when the output path is explicitly confirmed or safe to overwrite.
- Quote paths with spaces.

# Quick Reference - Common Tasks

## Get Video Information
```bash
ffprobe -v quiet -print_format json -show_format -show_streams "input.mp4"
```

## Convert Format
```bash
# MP4 to WebM (VP9 + Opus)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# Any format to MP4 (H.264 + AAC - most compatible)
ffmpeg -i input.mov -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4

# Convert to H.265/HEVC (smaller file, good quality)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -c:a aac output_hevc.mp4
```

## Compress Video
```bash
# Reduce file size (higher CRF = more compression, 18-28 is typical)
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -c:a aac -b:a 128k output.mp4

# Two-pass encoding for target file size
ffmpeg -i input.mp4 -c:v libx264 -b:v 1M -pass 1 -an -f null /dev/null && \
ffmpeg -i input.mp4 -c:v libx264 -b:v 1M -pass 2 -c:a aac -b:a 128k output.mp4
```

## Resize/Scale Video
```bash
# Scale to 1080p (maintain aspect ratio)
ffmpeg -i input.mp4 -vf "scale=-1:1080" -c:a copy output.mp4

# Scale to 720p width
ffmpeg -i input.mp4 -vf "scale=1280:-1" -c:a copy output.mp4

# Scale to exact dimensions (may stretch)
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# Scale with padding to fit exact dimensions
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

## Trim/Cut Video
```bash
# Cut from timestamp to timestamp (fast, no re-encode)
ffmpeg -ss 00:01:30 -to 00:02:45 -i input.mp4 -c copy output.mp4

# Cut with re-encoding (more accurate timestamps)
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:02:45 -c:v libx264 -c:a aac output.mp4

# Cut first N seconds
ffmpeg -i input.mp4 -t 30 -c copy output.mp4

# Skip first N seconds
ffmpeg -ss 10 -i input.mp4 -c copy output.mp4
```

## Extract/Replace Audio
```bash
# Extract audio to MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# Extract audio to WAV
ffmpeg -i input.mp4 -vn -acodec pcm_s16le output.wav

# Remove audio from video
ffmpeg -i input.mp4 -c:v copy -an output.mp4

# Replace audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Add audio to video (mix with original)
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[0:a][1:a]amix=inputs=2:duration=first" -c:v copy output.mp4
```

## Concatenate Videos
```bash
# Create a file list (files.txt):
# file 'video1.mp4'
# file 'video2.mp4'
# file 'video3.mp4'

# Concatenate (same codec)
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4

# Concatenate with re-encoding (different codecs/resolutions)
ffmpeg -f concat -safe 0 -i files.txt -c:v libx264 -c:a aac output.mp4
```

## Create GIF
```bash
# Simple GIF (low quality)
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" output.gif

# High quality GIF with palette
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif

# GIF from specific time range
ffmpeg -ss 00:00:05 -t 3 -i input.mp4 -vf "fps=15,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

## Change Framerate/Speed
```bash
# Change framerate
ffmpeg -i input.mp4 -filter:v fps=30 output.mp4

# Speed up video 2x
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" output.mp4

# Slow down video 0.5x
ffmpeg -i input.mp4 -filter:v "setpts=2.0*PTS" -filter:a "atempo=0.5" output.mp4
```

## Add Subtitles
```bash
# Burn subtitles into video (hardcoded)
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4

# Add subtitle stream (soft subs)
ffmpeg -i input.mp4 -i subs.srt -c:v copy -c:a copy -c:s mov_text output.mp4
```

## Add Text/Watermark
```bash
# Add text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10" output.mp4

# Add image watermark
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=10:10" output.mp4

# Add watermark bottom-right corner
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4
```

## Video Filters
```bash
# Rotate video
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4  # 90 clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4  # 90 counter-clockwise
ffmpeg -i input.mp4 -vf "hflip" output.mp4        # horizontal flip
ffmpeg -i input.mp4 -vf "vflip" output.mp4        # vertical flip

# Crop video (width:height:x:y)
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4

# Crop to center square
ffmpeg -i input.mp4 -vf "crop=min(iw\,ih):min(iw\,ih)" output.mp4

# Blur video
ffmpeg -i input.mp4 -vf "boxblur=5:1" output.mp4

# Sharpen video
ffmpeg -i input.mp4 -vf "unsharp=5:5:1.0:5:5:0.0" output.mp4

# Adjust brightness/contrast/saturation
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.mp4

# Denoise video
ffmpeg -i input.mp4 -vf "hqdn3d=4:3:6:4.5" output.mp4

# Color correction (curves)
ffmpeg -i input.mp4 -vf "curves=preset=lighter" output.mp4
```

## Video Stabilization
```bash
# Two-pass stabilization
ffmpeg -i input.mp4 -vf vidstabdetect -f null -
ffmpeg -i input.mp4 -vf vidstabtransform=smoothing=10 output.mp4
```

## Green Screen / Chroma Key
```bash
# Remove green background
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.1:0.2" -c:v png output.mov

# Replace green screen with another video
ffmpeg -i background.mp4 -i greenscreen.mp4 -filter_complex "[1:v]chromakey=0x00FF00:0.1:0.2[fg];[0:v][fg]overlay[out]" -map "[out]" output.mp4
```

## Extract Frames
```bash
# Extract all frames as images
ffmpeg -i input.mp4 frame_%04d.png

# Extract 1 frame per second
ffmpeg -i input.mp4 -vf fps=1 frame_%04d.png

# Extract single frame at timestamp
ffmpeg -ss 00:00:10 -i input.mp4 -frames:v 1 frame.png

# Extract thumbnail/poster
ffmpeg -i input.mp4 -ss 00:00:01 -frames:v 1 thumbnail.jpg
```

## Create Video from Images
```bash
# Images to video (image sequence)
ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4

# Single image to video with duration
ffmpeg -loop 1 -i image.png -c:v libx264 -t 10 -pix_fmt yuv420p output.mp4
```

## Screen Recording
```bash
# macOS screen capture
ffmpeg -f avfoundation -i "1" -r 30 -c:v libx264 output.mp4

# List available devices (macOS)
ffmpeg -f avfoundation -list_devices true -i ""
```

## Hardware Accelerated Encoding (macOS)
```bash
# H.264 with VideoToolbox (much faster)
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# HEVC with VideoToolbox
ffmpeg -i input.mp4 -c:v hevc_videotoolbox -b:v 5M output.mp4

# Check available hardware encoders
ffmpeg -encoders | grep videotoolbox
```

## Batch Processing
```bash
# Convert all MP4 files in a directory to WebM
for f in *.mp4; do ffmpeg -i "$f" -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus "${f%.mp4}.webm"; done

# Extract thumbnails from multiple videos
for f in *.mp4; do ffmpeg -i "$f" -ss 00:00:01 -frames:v 1 "${f%.mp4}_thumb.jpg"; done

# Compress all videos in directory
for f in *.mp4; do ffmpeg -i "$f" -c:v libx264 -crf 28 -preset fast -c:a aac "compressed_$f"; done
```

# Codec Quick Reference

| Codec | Encoder | Use Case |
|-------|---------|----------|
| H.264 | `libx264` | Most compatible, good quality/size |
| H.265/HEVC | `libx265` | Better compression, newer devices |
| VP9 | `libvpx-vp9` | WebM format, web streaming |
| AV1 | `libaom-av1` / `libsvtav1` | Best compression, slow encode |
| ProRes | `prores_ks` | Professional editing, large files |
| AAC | `aac` | Standard audio codec |
| MP3 | `libmp3lame` | Legacy audio format |
| Opus | `libopus` | Modern audio, web streaming |

# Quality Presets

## CRF (Constant Rate Factor)
- 0 = Lossless
- 18 = Visually lossless
- 23 = Default (good balance)
- 28 = Lower quality, smaller file
- 51 = Worst quality

## Encoding Presets (libx264/libx265)
- `ultrafast` - Fastest, largest file
- `fast` - Good balance for quick encodes
- `medium` - Default
- `slow` - Better compression
- `veryslow` - Best compression, very slow

# Common Issues & Solutions

## Audio/Video Sync Issues
```bash
# Re-encode with fixed timestamps
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -async 1 output.mp4
```

## Variable Frame Rate (VFR) to Constant Frame Rate (CFR)
```bash
ffmpeg -i input.mp4 -vsync cfr -r 30 output.mp4
```

## Fix Rotation Metadata
```bash
ffmpeg -i input.mp4 -c copy -metadata:s:v:0 rotate=0 output.mp4
```

## Convert for Web/HTML5
```bash
# MP4 for web (H.264 baseline, compatible with all browsers)
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p -c:a aac -movflags +faststart output.mp4
```

# Execution Notes
1. Analyze the input with ffprobe.
2. Prefer `-c copy` when no re-encode is needed.
3. Use a short clip test for long jobs.
4. Use `-y` only when the output path is confirmed safe to overwrite.

# Best Practices
- Quote file paths with spaces: `ffmpeg -i "my video.mp4" output.mp4`
- Use `-hide_banner` for cleaner output: `ffmpeg -hide_banner -i input.mp4 ...`
- Preserve metadata when copying: `ffmpeg -i input.mp4 -c copy -map_metadata 0 output.mp4`
- For web videos, add `-movflags +faststart` for progressive playback
- Check codec support before encoding: `ffmpeg -encoders | grep <codec>`

# Error Handling
```bash
# Check if ffmpeg is installed
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not installed"; exit 1; }

# Verify input file exists
[ -f "input.mp4" ] || { echo "Input file not found"; exit 1; }

# Check supported formats
ffmpeg -formats | grep <format>

# Verbose output for debugging
ffmpeg -v verbose -i input.mp4 output.mp4
```

# References
- `references/ffmpeg-filters.md` - Comprehensive filter reference
- `references/ffmpeg-codecs.md` - Detailed codec information
