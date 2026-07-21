#!/usr/bin/env python3
"""Render a dark and light animated terminal card for a GitHub profile README.

The daily GitHub Action runs this file with the Python standard library only.
Personal content lives in profile.json; portrait.txt is produced separately.
"""

from __future__ import annotations

import json
import os
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))

WIDTH = 1100
HEIGHT = 700
ART_X = 32
ART_Y = 94
ART_CHAR_WIDTH = 5.0
ART_LINE_HEIGHT = 8.3
INFO_X = 545
VALUE_X = 675
INFO_Y = 98
INFO_LINE_HEIGHT = 20
MAX_VALUE_CHARS = 46

THEMES = {
    "dark": {
        "background": "#050505",
        "panel": "#0a0a0a",
        "border": "#292524",
        "text": "#e7e5e4",
        "muted": "#a8a29e",
        "key": "#3fb950",
        "accent": "#58a6ff",
        "warning": "#d29922",
        "portrait": "#d97757",
    },
    "light": {
        "background": "#050505",
        "panel": "#0a0a0a",
        "border": "#292524",
        "text": "#e7e5e4",
        "muted": "#a8a29e",
        "key": "#3fb950",
        "accent": "#58a6ff",
        "warning": "#d29922",
        "portrait": "#d97757",
    },
}


def request_json(url: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "terminal-profile-readme",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def github_stats(username: str) -> dict[str, str]:
    fallback = {"repos": "—", "stars": "—", "followers": "—"}
    if not username or username == "YOUR_GITHUB_USERNAME":
        return fallback

    try:
        user = request_json(f"https://api.github.com/users/{username}")
        if not isinstance(user, dict):
            return fallback

        stars = 0
        page = 1
        while True:
            repos = request_json(
                f"https://api.github.com/users/{username}/repos"
                f"?type=owner&sort=updated&per_page=100&page={page}"
            )
            if not isinstance(repos, list) or not repos:
                break
            stars += sum(int(repo.get("stargazers_count", 0)) for repo in repos)
            if len(repos) < 100:
                break
            page += 1

        return {
            "repos": str(user.get("public_repos", 0)),
            "stars": str(stars),
            "followers": str(user.get("followers", 0)),
        }
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(f"warning: GitHub stats unavailable: {error}")
        return fallback


def portrait_lines() -> list[str]:
    portrait_path = ROOT / CONFIG.get("portrait_file", "portrait.txt")
    if not portrait_path.exists():
        return ["[ run photo_to_ascii.py with your photo ]"]
    return portrait_path.read_text(encoding="utf-8").rstrip().splitlines()


def local_timestamp() -> str:
    name = CONFIG.get("timezone", "UTC")
    try:
        zone = ZoneInfo(name)
    except ZoneInfoNotFoundError:
        print(f"warning: unknown timezone {name!r}; using UTC")
        zone = timezone.utc
    return datetime.now(zone).strftime("%d %b %Y · %H:%M %Z")


def value_lines(value: str, stats: dict[str, str]) -> list[str]:
    if value == "__github_stats__":
        value = (
            f"{stats['repos']} repos · {stats['stars']} stars · "
            f"{stats['followers']} followers"
        )
    return textwrap.wrap(
        value,
        width=MAX_VALUE_CHARS,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]


def render(theme_name: str, colors: dict[str, str], stats: dict[str, str]) -> str:
    username = str(CONFIG.get("github_username", "github"))
    name = str(CONFIG.get("display_name", username))
    command = str(CONFIG.get("command", "whoami --verbose"))
    title = str(CONFIG.get("window_title", "portfolio — zsh"))

    out = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
            f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
            f'aria-labelledby="title description">'
        ),
        f"<title id=\"title\">{escape(name)} — terminal profile</title>",
        (
            f'<desc id="description">Animated terminal-style GitHub profile card '
            f'for {escape(name)}.</desc>'
        ),
        f"""<style>
        text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
        .portrait {{ fill:{colors['portrait']}; font-size:7px; white-space:pre; }}
        .key {{ fill:{colors['key']}; font-size:14px; font-weight:700; }}
        .value {{ fill:{colors['text']}; font-size:14px; }}
        .accent {{ fill:{colors['accent']}; font-size:14px; }}
        .warning {{ fill:{colors['warning']}; font-size:14px; }}
        .muted {{ fill:{colors['muted']}; font-size:12px; }}
        .header {{ fill:{colors['accent']}; font-size:17px; font-weight:700; }}
        .section {{ fill:{colors['muted']}; font-size:12px; letter-spacing:1px; }}
        .row {{ opacity:1; animation:appear .35s ease backwards; }}
        .portrait-row {{ opacity:1; animation:appear .28s ease backwards; }}
        .cursor {{ fill:{colors['key']}; animation:blink 1s steps(1,end) infinite; }}
        @keyframes appear {{ from {{ opacity:0; transform:translateY(3px); }} to {{ opacity:1; transform:none; }} }}
        @keyframes blink {{ 50% {{ opacity:0; }} }}
        @media (prefers-reduced-motion: reduce) {{ .row,.portrait-row {{ opacity:1; animation:none; }} .cursor {{ animation:none; }} }}
        </style>""",
        (
            f'<rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="13" '
            f'fill="{colors["background"]}" stroke="{colors["border"]}" stroke-width="2"/>'
        ),
        (
            f'<path d="M1 14A13 13 0 0 1 14 1h{WIDTH - 28}a13 13 0 0 1 13 13v28H1Z" '
            f'fill="{colors["panel"]}"/>'
        ),
        f'<line x1="1" y1="42" x2="{WIDTH - 1}" y2="42" stroke="{colors["border"]}"/>',
    ]

    for x, color in zip((24, 44, 64), ("#ff5f56", "#ffbd2e", "#27c93f")):
        out.append(f'<circle cx="{x}" cy="22" r="6" fill="{color}"/>')
    out.append(
        f'<text x="{WIDTH / 2}" y="27" class="muted" text-anchor="middle">{escape(title)}</text>'
    )
    out.append(
        f'<text x="{ART_X}" y="70" class="row" style="animation-delay:.05s">'
        f'<tspan class="key">➜</tspan><tspan class="accent" dx="8">~</tspan>'
        f'<tspan class="value" dx="9">{escape(command)}</tspan></text>'
    )

    for index, line in enumerate(portrait_lines()):
        if not line.strip():
            continue
        y = ART_Y + index * ART_LINE_HEIGHT
        out.append(
            f'<text x="{ART_X}" y="{y:.1f}" class="portrait portrait-row" '
            f'xml:space="preserve" textLength="{len(line) * ART_CHAR_WIDTH:.1f}" '
            f'lengthAdjust="spacingAndGlyphs" style="animation-delay:{.12 + index * .012:.3f}s">'
            f'{escape(line)}</text>'
        )

    y = INFO_Y
    delay = 0.32
    out.append(
        f'<text x="{INFO_X}" y="{y}" class="header row" style="animation-delay:{delay}s">'
        f'{escape(name.lower())}</text>'
    )
    y += 20
    out.append(
        f'<line x1="{INFO_X}" y1="{y - 8}" x2="{WIDTH - 34}" y2="{y - 8}" '
        f'stroke="{colors["border"]}" class="row" style="animation-delay:{delay + .05}s"/>'
    )
    y += 10
    out.append(
        f'<text x="{INFO_X}" y="{y}" class="value row" style="animation-delay:{delay + .1}s">'
        f'{escape(str(CONFIG.get("headline", "")))}</text>'
    )
    y += 30
    delay += 0.18

    style_classes = {"value": "value", "accent": "accent", "warning": "warning", "muted": "muted"}
    for section in CONFIG.get("sections", []):
        out.append(
            f'<text x="{INFO_X}" y="{y}" class="section row" '
            f'style="animation-delay:{delay:.2f}s">{escape(str(section.get("title", "")))}</text>'
        )
        y += INFO_LINE_HEIGHT
        delay += .06
        for label, raw_value, style in section.get("items", []):
            lines = value_lines(str(raw_value), stats)
            out.append(
                f'<text x="{INFO_X}" y="{y}" class="key row" '
                f'style="animation-delay:{delay:.2f}s">{escape(str(label))}</text>'
            )
            for line_index, line in enumerate(lines):
                css_class = style_classes.get(str(style), "value")
                out.append(
                    f'<text x="{VALUE_X}" y="{y + line_index * INFO_LINE_HEIGHT}" '
                    f'class="{css_class} row" style="animation-delay:{delay:.2f}s">'
                    f'{escape(line)}</text>'
                )
            y += INFO_LINE_HEIGHT * len(lines)
            delay += .06
        y += 12

    footer_y = HEIGHT - 25
    out.append(
        f'<text x="{ART_X}" y="{footer_y}" class="row" style="animation-delay:{delay + .1:.2f}s">'
        f'<tspan class="key">➜</tspan><tspan class="accent" dx="8">~</tspan>'
        f'<tspan class="value" dx="9">{escape(str(CONFIG.get("footer", "")))}</tspan>'
        f'<tspan class="cursor" dx="8">█</tspan></text>'
    )
    out.append(
        f'<text x="{WIDTH - 28}" y="{footer_y}" class="muted" text-anchor="end">'
        f'updated {escape(local_timestamp())}</text>'
    )
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    username = str(CONFIG.get("github_username", ""))
    stats = github_stats(username)
    for theme_name, colors in THEMES.items():
        target = ROOT / f"profile-{theme_name}-cat.svg"
        target.write_text(render(theme_name, colors, stats), encoding="utf-8")
        print(f"wrote {target.name}")


if __name__ == "__main__":
    main()
