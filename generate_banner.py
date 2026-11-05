"""Render assets/banner.svg: an ASCII name banner with a typing animation.

Pure SVG + SMIL (no JavaScript), so it animates inside GitHub's <img> rendering.
Run: python generate_banner.py
"""
from html import escape
from pathlib import Path

ART = r"""
    _    _           _       ____
   / \  | | _____  _(_)___  |  _ \ ___ _   _ _ __   __ _
  / _ \ | |/ _ \ \/ / / __| | |_) / _ \ | | | '_ \ / _` |
 / ___ \| |  __/>  <| \__ \ |  _ <  __/ |_| | | | | (_| |
/_/   \_\_|\___/_/\_\_|___/ |_| \_\___|\__, |_| |_|\__,_|
                                       |___/
""".strip("\n").split("\n")
TAGLINE = "DevOps, Cloud Engineer, and Software Developer"
PROMPT = "$ npx alexisrs"

BG, FG = "#0d1117", "#b3b3b3"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
CHAR = 0.6  # monospace advance width, in em

W = 900
ART_SIZE, ART_LEAD = 21.6, 24.3
TAG_SIZE, PROMPT_SIZE = 18, 20

# Typing timeline (seconds)
ART_START, ART_STEP = 0.3, 0.035
TAG_GAP, TAG_STEP = 0.25, 0.03
PROMPT_GAP, PROMPT_STEP = 0.35, 0.09


def nbsp(text):
    return escape(text, quote=False).replace(" ", "&#160;")


def typing_clip(cid, x, y, height, chars, char_w, begin, step):
    """A clipPath whose width grows one character at a time."""
    values = ";".join(f"{i * char_w:.2f}" for i in range(chars + 1))
    dur = step * (chars + 1)
    return (
        f'    <clipPath id="{cid}"><rect x="{x:.2f}" y="{y:.2f}" width="0" height="{height:.2f}">'
        f'<animate attributeName="width" values="{values}" calcMode="discrete" '
        f'begin="{begin:.3f}s" dur="{dur:.3f}s" fill="freeze"/></rect></clipPath>'
    ), begin + step * chars


def main():
    cols = max(len(line) for line in ART)
    art = [line.ljust(cols) for line in ART]
    art_cw = ART_SIZE * CHAR
    art_w = cols * art_cw
    x0 = (W - art_w) / 2
    x1 = x0 + art_w

    y0 = 64
    art_bottom = y0 + (len(art) - 1) * ART_LEAD
    tag_y = art_bottom + 48
    prompt_y = tag_y + 50
    H = round(prompt_y + 40)

    tag_cw = TAG_SIZE * CHAR
    tag_w = len(TAGLINE) * tag_cw
    prompt_cw = PROMPT_SIZE * CHAR
    prompt_w = len(PROMPT) * prompt_cw

    art_clip, art_end = typing_clip("type-art", x0, y0 - ART_SIZE, art_bottom - y0 + ART_SIZE * 1.4,
                                    cols, art_cw, ART_START, ART_STEP)
    tag_begin = art_end + TAG_GAP
    tag_clip, tag_end = typing_clip("type-tag", x1 - tag_w, tag_y - TAG_SIZE, TAG_SIZE * 1.5,
                                    len(TAGLINE), tag_cw, tag_begin, TAG_STEP)
    prompt_begin = tag_end + PROMPT_GAP
    prompt_clip, prompt_end = typing_clip("type-prompt", x0, prompt_y - PROMPT_SIZE, PROMPT_SIZE * 1.5,
                                          len(PROMPT), prompt_cw, prompt_begin, PROMPT_STEP)

    # Block cursor that follows the prompt as it is typed, then blinks forever.
    cursor_xs = ";".join(f"{x0 + (i + 1) * prompt_cw + 2:.2f}" for i in range(-1, len(PROMPT)))
    cursor = (
        f'  <rect x="{x0:.2f}" y="{prompt_y - PROMPT_SIZE * 0.82:.2f}" width="{prompt_cw:.2f}" '
        f'height="{PROMPT_SIZE:.2f}" fill="{FG}" opacity="0">\n'
        f'    <set attributeName="opacity" to="1" begin="{prompt_begin - PROMPT_GAP:.3f}s"/>\n'
        f'    <animate attributeName="x" values="{cursor_xs}" calcMode="discrete" '
        f'begin="{prompt_begin:.3f}s" dur="{PROMPT_STEP * (len(PROMPT) + 1):.3f}s" fill="freeze"/>\n'
        f'    <animate attributeName="opacity" values="1;0" calcMode="discrete" '
        f'begin="{prompt_end + 0.4:.3f}s" dur="1.06s" repeatCount="indefinite"/>\n'
        f'  </rect>'
    )

    rows = "\n".join(
        f'      <text x="{x0:.2f}" y="{y0 + i * ART_LEAD:.2f}" textLength="{art_w:.2f}" '
        f'lengthAdjust="spacing">{nbsp(line)}</text>'
        for i, line in enumerate(art)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Alexis Reyna — {escape(TAGLINE)} — {escape(PROMPT)}">
  <defs>
{art_clip}
{tag_clip}
{prompt_clip}
  </defs>
  <rect width="100%" height="100%" rx="8" fill="{BG}"/>
  <g font-family="{FONT}" fill="{FG}" xml:space="preserve" style="white-space:pre">
    <g font-size="{ART_SIZE}" clip-path="url(#type-art)">
{rows}
    </g>
    <text x="{x1 - tag_w:.2f}" y="{tag_y:.2f}" font-size="{TAG_SIZE}" font-weight="bold" textLength="{tag_w:.2f}" lengthAdjust="spacing" clip-path="url(#type-tag)">{nbsp(TAGLINE)}</text>
    <text x="{x0:.2f}" y="{prompt_y:.2f}" font-size="{PROMPT_SIZE}" font-weight="bold" textLength="{prompt_w:.2f}" lengthAdjust="spacing" clip-path="url(#type-prompt)">{nbsp(PROMPT)}</text>
  </g>
{cursor}
</svg>
"""
    Path(__file__).with_name("assets").joinpath("banner.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
