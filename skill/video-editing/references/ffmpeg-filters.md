# FFmpeg Video Filters Reference

This document provides detailed examples of commonly used ffmpeg video filters.

## Filter Syntax

Filters are applied using the `-vf` (video filter) or `-af` (audio filter) flags, or `-filter_complex` for complex filtergraphs.

```bash
# Single filter
ffmpeg -i input.mp4 -vf "filtername=param1=value1:param2=value2" output.mp4

# Multiple filters (chained)
ffmpeg -i input.mp4 -vf "filter1,filter2,filter3" output.mp4

# Complex filtergraph (multiple inputs/outputs)
ffmpeg -i input1.mp4 -i input2.mp4 -filter_complex "[0:v][1:v]overlay[out]" -map "[out]" output.mp4
```

## Video Transformation Filters

### scale - Resize Video
```bash
# Scale to width 1280, auto height (maintain aspect ratio)
-vf "scale=1280:-1"

# Scale to height 720, auto width
-vf "scale=-1:720"

# Scale to exact dimensions
-vf "scale=1920:1080"

# Scale with high quality algorithm
-vf "scale=1280:720:flags=lanczos"

# Scale to fit within bounds (no stretch)
-vf "scale=1920:1080:force_original_aspect_ratio=decrease"

# Scale to fill bounds (may crop)
-vf "scale=1920:1080:force_original_aspect_ratio=increase"

# Scale to even dimensions (required for many codecs)
-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"
```

### crop - Crop Video
```bash
# Crop to width:height starting at x:y
-vf "crop=640:480:100:50"

# Crop center region
-vf "crop=640:480"

# Crop to 16:9 aspect ratio (center)
-vf "crop=ih*16/9:ih"

# Crop to square (center)
-vf "crop=min(iw\,ih):min(iw\,ih)"

# Remove 10 pixels from each edge
-vf "crop=iw-20:ih-20:10:10"
```

### pad - Add Padding/Letterbox
```bash
# Add black bars to fit 16:9
-vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black"

# Add padding to top and bottom
-vf "pad=iw:ih+100:0:50:black"

# Add colored padding
-vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white"
```

### transpose - Rotate Video
```bash
# Rotate 90 degrees clockwise
-vf "transpose=1"

# Rotate 90 degrees counter-clockwise
-vf "transpose=2"

# Rotate 90 clockwise and flip vertically
-vf "transpose=3"

# Rotate 180 degrees
-vf "transpose=1,transpose=1"

# Horizontal flip (mirror)
-vf "hflip"

# Vertical flip
-vf "vflip"

# Rotate arbitrary angle (in radians, with black background)
-vf "rotate=PI/4:fillcolor=black"

# Rotate arbitrary angle (in degrees)
-vf "rotate=45*PI/180"
```

## Color and Enhancement Filters

### eq - Brightness/Contrast/Saturation
```bash
# Adjust brightness (-1.0 to 1.0, default 0)
-vf "eq=brightness=0.2"

# Adjust contrast (0 to 2.0, default 1)
-vf "eq=contrast=1.3"

# Adjust saturation (0 to 3.0, default 1)
-vf "eq=saturation=1.5"

# Adjust gamma (0.1 to 10, default 1)
-vf "eq=gamma=1.2"

# Combined adjustments
-vf "eq=brightness=0.1:contrast=1.2:saturation=1.3:gamma=0.9"
```

### curves - Color Curves
```bash
# Apply preset
-vf "curves=preset=lighter"
-vf "curves=preset=darker"
-vf "curves=preset=increase_contrast"
-vf "curves=preset=strong_contrast"
-vf "curves=preset=vintage"
-vf "curves=preset=negative"

# Custom curve (all channels)
-vf "curves=all='0/0 0.5/0.4 1/1'"

# Per-channel curves
-vf "curves=red='0/0 0.5/0.6 1/1':green='0/0 1/1':blue='0/0 0.5/0.4 1/1'"
```

### colorbalance - Color Balance
```bash
# Adjust shadows/midtones/highlights for RGB
-vf "colorbalance=rs=0.3:gs=-0.1:bs=0.1:rm=0.1:gm=-0.1:bm=0.1"
```

### colortemperature - White Balance
```bash
# Warmer (higher temperature)
-vf "colortemperature=temperature=7000"

# Cooler (lower temperature)
-vf "colortemperature=temperature=4000"
```

### vibrance - Saturation Enhancement
```bash
# Boost vibrance (avoids oversaturating already saturated colors)
-vf "vibrance=intensity=0.5"
```

### hue - Hue/Saturation Adjustment
```bash
# Rotate hue (degrees)
-vf "hue=h=90"

# Adjust saturation
-vf "hue=s=2"

# Combined
-vf "hue=h=30:s=1.5"
```

## Blur and Sharpen Filters

### boxblur - Box Blur
```bash
# Simple blur
-vf "boxblur=5:1"

# Separate horizontal and vertical
-vf "boxblur=luma_radius=3:luma_power=2:chroma_radius=2:chroma_power=1"
```

### gblur - Gaussian Blur
```bash
# Gaussian blur
-vf "gblur=sigma=10"
```

### unsharp - Sharpen/Blur
```bash
# Sharpen
-vf "unsharp=5:5:1.0:5:5:0.0"

# Strong sharpen
-vf "unsharp=7:7:2.5:7:7:1.0"

# Blur (negative values)
-vf "unsharp=5:5:-1.0:5:5:-1.0"
```

### cas - Contrast Adaptive Sharpen
```bash
# Subtle sharpening
-vf "cas=strength=0.5"

# Strong sharpening
-vf "cas=strength=1.0"
```

## Noise and Denoise Filters

### hqdn3d - High Quality Denoise
```bash
# Light denoise
-vf "hqdn3d=2:2:3:3"

# Medium denoise
-vf "hqdn3d=4:3:6:4.5"

# Strong denoise
-vf "hqdn3d=8:6:12:9"
```

### nlmeans - Non-Local Means Denoise
```bash
# Standard denoise
-vf "nlmeans=s=3.0:p=7:r=15"
```

### noise - Add Noise
```bash
# Add film grain
-vf "noise=alls=20:allf=t+u"
```

## Overlay and Composition Filters

### overlay - Composite Videos/Images
```bash
# Overlay at position
-filter_complex "[0:v][1:v]overlay=10:10"

# Overlay centered
-filter_complex "[0:v][1:v]overlay=(W-w)/2:(H-h)/2"

# Overlay bottom-right corner
-filter_complex "[0:v][1:v]overlay=W-w-10:H-h-10"

# Overlay with transparency
-filter_complex "[0:v][1:v]overlay=10:10:format=auto"
```

### drawtext - Text Overlay
```bash
# Simple text
-vf "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10"

# Centered text
-vf "drawtext=text='Centered':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"

# Text with background box
-vf "drawtext=text='With Box':fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=10"

# Custom font
-vf "drawtext=text='Custom Font':fontfile=/path/to/font.ttf:fontsize=36:fontcolor=yellow:x=100:y=100"

# Timecode overlay
-vf "drawtext=text='%{pts\\:hms}':fontsize=24:fontcolor=white:x=10:y=10"

# Frame number
-vf "drawtext=text='%{frame_num}':fontsize=24:fontcolor=white:x=10:y=10"
```

### drawbox - Draw Rectangle
```bash
# Draw box
-vf "drawbox=x=100:y=100:w=200:h=150:color=red@0.5:t=fill"

# Draw border only
-vf "drawbox=x=100:y=100:w=200:h=150:color=blue:t=5"
```

## Chroma Key Filters

### chromakey - Remove Color (YUV)
```bash
# Remove green screen
-vf "chromakey=0x00FF00:0.1:0.2"

# Remove blue screen
-vf "chromakey=0x0000FF:0.1:0.2"
```

### colorkey - Remove Color (RGB)
```bash
# Remove green
-vf "colorkey=0x00FF00:0.1:0.2"
```

## Time Filters

### setpts - Change Speed
```bash
# 2x speed (half duration)
-vf "setpts=0.5*PTS"

# 0.5x speed (double duration)
-vf "setpts=2.0*PTS"

# Reverse video
-vf "reverse"
```

### fps - Change Framerate
```bash
# Set output framerate
-vf "fps=30"

# Convert 60fps to 24fps with frame blending
-vf "fps=24"
```

### trim - Cut Video
```bash
# Trim to range (in seconds)
-vf "trim=start=10:end=20,setpts=PTS-STARTPTS"

# Trim by frame count
-vf "trim=start_frame=100:end_frame=200,setpts=PTS-STARTPTS"
```

### loop - Loop Video
```bash
# Loop 5 times
-vf "loop=loop=5:size=1000:start=0"
```

## Transition Filters

### xfade - Cross Fade
```bash
# Cross fade between two videos
-filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]"

# Available transitions: fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, distance, fadeblack, fadewhite, radial, smoothleft, smoothright, smoothup, smoothdown, circleopen, circleclose, vertopen, vertclose, horzopen, horzclose, dissolve, pixelize, diagtl, diagtr, diagbl, diagbr, hlslice, hrslice, vuslice, vdslice, hblur, fadegrays, wipetl, wipetr, wipebl, wipebr, squeezeh, squeezev, zoomin
```

### fade - Fade In/Out
```bash
# Fade in (first 30 frames)
-vf "fade=t=in:st=0:d=1"

# Fade out (last second)
-vf "fade=t=out:st=9:d=1"

# Both fade in and out
-vf "fade=t=in:st=0:d=0.5,fade=t=out:st=9.5:d=0.5"
```

## Edge Detection and Artistic

### edgedetect - Edge Detection
```bash
# Basic edge detection
-vf "edgedetect"

# Colored edges
-vf "edgedetect=mode=colormix"
```

### negate - Invert Colors
```bash
-vf "negate"
```

### vignette - Vignette Effect
```bash
# Add vignette
-vf "vignette"

# Custom vignette
-vf "vignette=PI/4"
```

### deshake - Video Stabilization
```bash
# Basic stabilization
-vf "deshake"
```

### vidstab - Advanced Stabilization (Two-Pass)
```bash
# Pass 1: Analyze
ffmpeg -i input.mp4 -vf vidstabdetect=shakiness=10:accuracy=15 -f null -

# Pass 2: Transform
ffmpeg -i input.mp4 -vf vidstabtransform=smoothing=30:zoom=5 output.mp4
```

## Audio Filters

### volume - Adjust Volume
```bash
# Double volume
-af "volume=2.0"

# Half volume
-af "volume=0.5"

# Volume in dB
-af "volume=3dB"
```

### atempo - Change Audio Speed
```bash
# 2x speed
-af "atempo=2.0"

# 0.5x speed
-af "atempo=0.5"

# More than 2x (chain filters)
-af "atempo=2.0,atempo=2.0"  # 4x speed
```

### afade - Audio Fade
```bash
# Fade in
-af "afade=t=in:st=0:d=3"

# Fade out
-af "afade=t=out:st=7:d=3"
```

### loudnorm - Loudness Normalization
```bash
# Normalize to broadcast standards
-af "loudnorm=I=-16:TP=-1.5:LRA=11"
```

### aecho - Add Echo
```bash
# Simple echo
-af "aecho=0.8:0.9:1000:0.3"
```

### equalizer - Audio EQ
```bash
# Boost bass
-af "equalizer=f=100:width_type=o:width=2:g=5"

# Cut high frequencies
-af "equalizer=f=8000:width_type=o:width=2:g=-10"
```
