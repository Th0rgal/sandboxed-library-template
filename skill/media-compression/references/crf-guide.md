# CRF (Constant Rate Factor) Guide

CRF controls quality vs file size trade-off. Lower CRF = higher quality, larger file.

## H.264 (libx264)

| CRF | Quality | Use Case |
|-----|---------|----------|
| 0 | Lossless | Archival only |
| 18 | Visually lossless | High-quality preservation |
| 20 | Excellent | Recommended for quality |
| 23 | Good (default) | Balanced quality/size |
| 28 | Acceptable | Maximum compression |
| 51 | Worst | Not recommended |

**Recommended: CRF 18-23**

## H.265/HEVC (libx265)

H.265 achieves similar quality at higher CRF values (better compression).

| CRF | Quality | Equivalent H.264 |
|-----|---------|------------------|
| 0 | Lossless | — |
| 20 | Visually lossless | ~18 |
| 24 | Excellent | ~20 |
| 28 | Good (default) | ~23 |
| 32 | Acceptable | ~28 |

**Recommended: CRF 20-28**

## VP9 (libvpx-vp9)

| CRF | Quality | Use Case |
|-----|---------|----------|
| 0 | Lossless | Archival |
| 15-20 | Very high | Premium quality |
| 25-30 | High | Recommended |
| 35-40 | Medium | Web delivery |
| 50-63 | Low | Maximum compression |

**Recommended: CRF 25-35**

Note: VP9 requires `-b:v 0` to enable CRF mode.

## WebP Quality

WebP uses `-quality` (0-100) instead of CRF:

| Quality | Result |
|---------|--------|
| 100 | Highest quality, larger file |
| 90 | Near-lossless, excellent compression |
| 85 | Great for photos |
| 75 | Good balance |
| 50 | Noticeable artifacts |

**Recommended: 85-95 for photos, 90+ for graphics**

Use `-lossless 1` for mathematically identical output (PNG replacement).
