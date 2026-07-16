#!/usr/bin/env python3
"""Convert a portrait photo to a transparent-background ASCII bust.

Install the local-only dependencies first:
    python -m pip install -r requirements-portrait.txt

Then run:
    python photo_to_ascii.py path/to/your-photo.jpg
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import new_session, remove


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photo", type=Path, help="JPG, PNG, or WEBP portrait")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("portrait.txt"))
    parser.add_argument("--columns", type=int, default=92, help="ASCII width")
    parser.add_argument("--bust", type=float, default=0.68, help="fraction of subject height to retain")
    parser.add_argument("--detail", type=float, default=2.25, help="local-contrast gain")
    parser.add_argument("--shape", type=float, default=0.42, help="global light/dark weight")
    parser.add_argument("--threshold", type=int, default=105, help="alpha-mask cutoff")
    parser.add_argument(
        "--trim-x",
        type=float,
        default=0,
        help="trim this fraction from both sides of the detected bust to zoom in",
    )
    parser.add_argument(
        "--model",
        default="u2net_human_seg",
        help="rembg model; u2net_human_seg works best for portraits",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.photo.exists():
        raise SystemExit(f"photo not found: {args.photo}")

    session = new_session(args.model)
    subject = remove(Image.open(args.photo).convert("RGBA"), session=session)
    rgba = np.asarray(subject)
    alpha = rgba[:, :, 3]
    ys, xs = np.nonzero(alpha > 60)
    if len(xs) == 0:
        raise SystemExit("background removal found no subject; try a clearer portrait")

    y0, subject_bottom = int(ys.min()), int(ys.max())
    y1 = int(y0 + (subject_bottom - y0) * args.bust)
    retained = alpha[y0:y1, :] > 60
    _, retained_xs = np.nonzero(retained)
    x0, x1 = int(retained_xs.min()), int(retained_xs.max())
    horizontal_trim = int((x1 - x0) * args.trim_x)
    x0 += horizontal_trim
    x1 -= horizontal_trim
    pad = max(6, int((x1 - x0) * .025))
    box = (
        max(0, x0 - pad),
        max(0, y0 - pad),
        min(rgba.shape[1], x1 + pad),
        min(rgba.shape[0], y1),
    )
    subject = subject.crop(box)

    alpha_float = np.asarray(subject)[:, :, 3].astype(np.float32) / 255
    gray = np.asarray(ImageOps.autocontrast(subject.convert("L"), cutoff=1), dtype=np.float32)
    blur_radius = max(2, gray.shape[1] // 55)
    blur = np.asarray(
        Image.fromarray(gray.astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur_radius)),
        dtype=np.float32,
    )
    ink = np.clip(150 + (gray - blur) * args.detail + (gray - 128) * args.shape, 0, 255)

    inside = alpha_float > .5
    low, high = np.percentile(ink[inside], (2, 98))
    ink = np.clip((ink - low) * 255 / max(1, high - low), 0, 255)

    aspect_correction = 1.66
    rows = max(1, int(args.columns * gray.shape[0] / gray.shape[1] / aspect_correction))
    small_ink = np.asarray(
        Image.fromarray(ink.astype(np.uint8)).resize((args.columns, rows), Image.Resampling.LANCZOS),
        dtype=np.float32,
    )
    small_mask = np.asarray(
        Image.fromarray((alpha_float * 255).astype(np.uint8)).resize(
            (args.columns, rows), Image.Resampling.LANCZOS
        ),
        dtype=np.float32,
    )

    ramp = "@%#*+=-:. "
    last = len(ramp) - 1
    lines = []
    for row in range(rows):
        line = "".join(
            ramp[round(small_ink[row, col] / 255 * last)]
            if small_mask[row, col] > args.threshold
            else " "
            for col in range(args.columns)
        )
        lines.append(line.rstrip())

    args.output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {args.output} ({args.columns} columns × {rows} rows)")


if __name__ == "__main__":
    main()
