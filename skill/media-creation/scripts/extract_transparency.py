#!/usr/bin/env python3
"""
Transparency Extraction from Multiple Solid Background Images

This script extracts true RGBA values from images rendered on different
solid color backgrounds (black, white, and optionally red).

Mathematical basis:
For a pixel with true color C and alpha A, composited over background B:
    Result = C * A + B * (1 - A)

With black background (B=0): R_black = C * A
With white background (B=1): R_white = C * A + (1 - A)

Solving:
    R_white - R_black = 1 - A
    A = 1 - (R_white - R_black)
    C = R_black / A  (when A > 0)

The third background (red) provides additional constraints for better accuracy,
especially for pixels where the color is close to black or white.
"""

from __future__ import annotations

import argparse
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple


def load_image(path: Path) -> np.ndarray:
    """Load image and convert to float32 array normalized to [0, 1]."""
    img = Image.open(path).convert("RGB")
    return np.array(img, dtype=np.float32) / 255.0


def extract_alpha_from_two_backgrounds(
    img_black: np.ndarray,
    img_white: np.ndarray,
) -> np.ndarray:
    """
    Extract alpha channel using black and white backgrounds.
    
    For each channel:
        alpha = 1 - (white - black)
    
    We average across RGB channels for more robust alpha estimation.
    """
    # Calculate alpha for each channel
    alpha_per_channel = 1.0 - (img_white - img_black)
    
    # Average alpha across channels (they should be similar)
    alpha = np.mean(alpha_per_channel, axis=2)
    
    # Clamp to valid range
    alpha = np.clip(alpha, 0.0, 1.0)
    
    return alpha


def extract_alpha_with_three_backgrounds(
    img_black: np.ndarray,
    img_white: np.ndarray,
    img_colored: np.ndarray,
    bg_color: Tuple[float, float, float],
) -> np.ndarray:
    """
    Extract alpha using three backgrounds for improved accuracy.
    
    Uses least squares fitting across all three backgrounds to find
    the best alpha value that explains all observations.
    """
    h, w, c = img_black.shape
    
    # Stack all observations: shape (3, H, W, C)
    observations = np.stack([img_black, img_white, img_colored], axis=0)
    
    # Background colors: shape (3, C)
    backgrounds = np.array([
        [0.0, 0.0, 0.0],  # black
        [1.0, 1.0, 1.0],  # white
        list(bg_color),   # colored (e.g., red)
    ], dtype=np.float32)
    
    # For each pixel, we want to find alpha that minimizes error
    # Result_i = C * A + B_i * (1 - A)
    # Rearranging: Result_i = C * A + B_i - B_i * A = B_i + A * (C - B_i)
    
    # From black and white, we can get a good initial estimate
    alpha_initial = extract_alpha_from_two_backgrounds(img_black, img_white)
    
    # Refine using the colored background
    # For colored bg: Result_colored = C * A + bg_color * (1 - A)
    # We know C * A = img_black (from black bg)
    # So: Result_colored = img_black + bg_color * (1 - A)
    # Therefore: A = 1 - (Result_colored - img_black) / bg_color
    
    # Calculate alpha from each color channel of the colored background
    bg_color_arr = np.array(bg_color, dtype=np.float32)
    
    # Only use channels where background color is significantly non-zero
    alpha_estimates = []
    alpha_estimates.append(alpha_initial)
    
    for ch in range(3):
        if bg_color_arr[ch] > 0.1:  # Only use this channel if bg has significant color
            alpha_ch = 1.0 - (img_colored[:, :, ch] - img_black[:, :, ch]) / bg_color_arr[ch]
            alpha_ch = np.clip(alpha_ch, 0.0, 1.0)
            alpha_estimates.append(alpha_ch)
    
    # Weighted average of all alpha estimates
    # Give more weight to the black/white estimate as it's generally more reliable
    alpha = alpha_estimates[0] * 0.5
    if len(alpha_estimates) > 1:
        weight_per_colored = 0.5 / (len(alpha_estimates) - 1)
        for i in range(1, len(alpha_estimates)):
            alpha += alpha_estimates[i] * weight_per_colored
    
    return np.clip(alpha, 0.0, 1.0)


def extract_color(
    img_black: np.ndarray,
    alpha: np.ndarray,
    epsilon: float = 1e-6,
) -> np.ndarray:
    """
    Extract the true premultiplied color from the black background image.
    
    Since Result_black = C * A, we have C = Result_black / A
    """
    h, w, c = img_black.shape
    
    # Expand alpha to match color dimensions
    alpha_expanded = alpha[:, :, np.newaxis]
    
    # Avoid division by zero
    safe_alpha = np.maximum(alpha_expanded, epsilon)
    
    # Extract color
    color = img_black / safe_alpha
    
    # For fully transparent pixels, set color to 0
    color = np.where(alpha_expanded > epsilon, color, 0.0)
    
    # Clamp to valid range
    color = np.clip(color, 0.0, 1.0)
    
    return color


def create_rgba_image(color: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Combine color and alpha into RGBA image."""
    h, w, _ = color.shape
    
    # Create RGBA array
    rgba = np.zeros((h, w, 4), dtype=np.float32)
    rgba[:, :, :3] = color
    rgba[:, :, 3] = alpha
    
    return rgba


def save_rgba_image(rgba: np.ndarray, path: Path):
    """Save RGBA array as PNG with transparency."""
    # Convert to uint8
    rgba_uint8 = (rgba * 255).astype(np.uint8)
    
    # Create PIL image and save
    img = Image.fromarray(rgba_uint8)
    img = img.convert("RGBA")
    img.save(path, "PNG")


def extract_transparency(
    black_path: Path,
    white_path: Path,
    colored_path: Optional[Path] = None,
    colored_bg: Tuple[float, float, float] = (1.0, 0.0, 0.0),
    output_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Main function to extract transparency from background images.
    
    Args:
        black_path: Path to image on black background
        white_path: Path to image on white background
        colored_path: Optional path to image on colored background
        colored_bg: RGB tuple (0-1) of the colored background
        output_path: Path to save the result
    
    Returns:
        RGBA numpy array of the extracted image
    """
    print(f"Loading images...")
    img_black = load_image(black_path)
    img_white = load_image(white_path)
    
    print(f"  Black: {img_black.shape}")
    print(f"  White: {img_white.shape}")
    
    # Verify dimensions match
    if img_black.shape != img_white.shape:
        raise ValueError("Black and white images must have the same dimensions")
    
    # Extract alpha
    if colored_path is not None:
        img_colored = load_image(colored_path)
        print(f"  Colored: {img_colored.shape}")
        
        if img_colored.shape != img_black.shape:
            raise ValueError("All images must have the same dimensions")
        
        print(f"Extracting alpha using three backgrounds...")
        alpha = extract_alpha_with_three_backgrounds(
            img_black, img_white, img_colored, colored_bg
        )
    else:
        print(f"Extracting alpha using two backgrounds...")
        alpha = extract_alpha_from_two_backgrounds(img_black, img_white)
    
    # Extract color
    print(f"Extracting color...")
    color = extract_color(img_black, alpha)
    
    # Combine into RGBA
    rgba = create_rgba_image(color, alpha)
    
    # Print statistics
    print(f"\nStatistics:")
    print(f"  Alpha range: [{alpha.min():.4f}, {alpha.max():.4f}]")
    print(f"  Fully transparent pixels: {np.sum(alpha < 0.01):,}")
    print(f"  Fully opaque pixels: {np.sum(alpha > 0.99):,}")
    print(f"  Semi-transparent pixels: {np.sum((alpha >= 0.01) & (alpha <= 0.99)):,}")
    
    # Save if output path provided
    if output_path is not None:
        print(f"\nSaving to {output_path}...")
        save_rgba_image(rgba, output_path)
        print(f"Done!")
    
    return rgba


def create_checkerboard(width: int, height: int, tile_size: int = 16) -> np.ndarray:
    """Create a checkerboard pattern for transparency visualization."""
    # Create tile pattern
    light = 0.9
    dark = 0.7
    
    # Calculate number of tiles
    tiles_x = (width + tile_size - 1) // tile_size
    tiles_y = (height + tile_size - 1) // tile_size
    
    # Create pattern
    pattern = np.zeros((tiles_y, tiles_x), dtype=np.float32)
    pattern[0::2, 0::2] = light
    pattern[1::2, 1::2] = light
    pattern[0::2, 1::2] = dark
    pattern[1::2, 0::2] = dark
    
    # Scale up to pixel size
    checker = np.repeat(np.repeat(pattern, tile_size, axis=0), tile_size, axis=1)
    checker = checker[:height, :width]
    
    # Make RGB
    return np.stack([checker, checker, checker], axis=2)


def composite_over_checkerboard(rgba: np.ndarray, tile_size: int = 16) -> np.ndarray:
    """Composite RGBA image over checkerboard for transparency visualization."""
    h, w = rgba.shape[:2]
    checker = create_checkerboard(w, h, tile_size)
    
    color = rgba[:, :, :3]
    alpha = rgba[:, :, 3:4]
    
    result = color * alpha + checker * (1 - alpha)
    return result


def create_preview(rgba: np.ndarray, max_size: int = 512) -> Image.Image:
    """Create a downscaled preview of the RGBA image with checkerboard background."""
    h, w = rgba.shape[:2]
    scale = min(max_size / max(h, w), 1.0)
    new_h, new_w = int(h * scale), int(w * scale)
    
    rgba_uint8 = (rgba * 255).astype(np.uint8)
    img = Image.fromarray(rgba_uint8).convert("RGBA")
    
    if scale < 1.0:
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        rgba_small = np.array(img, dtype=np.float32) / 255.0
    else:
        rgba_small = rgba
    
    # Create checkerboard composite for visualization
    checker_composite = composite_over_checkerboard(rgba_small, tile_size=8)
    checker_uint8 = (checker_composite * 255).astype(np.uint8)
    
    return Image.fromarray(checker_uint8).convert("RGB")


def main():
    parser = argparse.ArgumentParser(
        description="Extract transparency from images on solid backgrounds"
    )
    parser.add_argument(
        "--black", "-b",
        type=Path,
        default=Path(__file__).parent / "black.jpeg",
        help="Path to image on black background"
    )
    parser.add_argument(
        "--white", "-w",
        type=Path,
        default=Path(__file__).parent / "white.jpeg",
        help="Path to image on white background"
    )
    parser.add_argument(
        "--colored", "-c",
        type=Path,
        default=None,
        help="Path to image on colored background (optional)"
    )
    parser.add_argument(
        "--colored-rgb",
        type=float,
        nargs=3,
        default=[1.0, 0.0, 0.0],
        metavar=("R", "G", "B"),
        help="RGB values (0-1) of the colored background (default: 1 0 0 for red)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path(__file__).parent / "output.png",
        help="Output path for the transparent PNG"
    )
    parser.add_argument(
        "--preview-size",
        type=int,
        default=512,
        help="Max size for preview images"
    )
    
    args = parser.parse_args()
    
    # Use red.jpeg as default colored image if it exists
    if args.colored is None:
        default_red = Path(__file__).parent / "red.jpeg"
        if default_red.exists():
            args.colored = default_red
    
    rgba = extract_transparency(
        black_path=args.black,
        white_path=args.white,
        colored_path=args.colored,
        colored_bg=tuple(args.colored_rgb),
        output_path=args.output,
    )
    
    # Create and save preview
    preview_path = args.output.with_stem(args.output.stem + "_preview")
    preview = create_preview(rgba, args.preview_size)
    preview.save(preview_path, "PNG")
    print(f"Preview saved to {preview_path}")


if __name__ == "__main__":
    main()

