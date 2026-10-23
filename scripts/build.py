"""Renders the org page images from design/*.html with headless Chromium.

Run: python3 scripts/build.py
Writes profile/assets/{banner,how-it-fits}-{dark,light}.png and social/<repo>.png.
Fonts are drawn here because GitHub's <img> SVG renderer can't load web fonts.
"""
import html
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
SCALE = 2

# name: (eyebrow, title, package, tagline, panel head, rows, exit line)
SOCIAL = {
    "notifications": (
        "bring your own", "Notifications", "@byo-oss/notifications",
        "A bell, an inbox and email follow-up for anything that went unread.",
        "inbox", [("● Payment failed", "2m"), ("○ Invite accepted", "1h")], "exit → Knock · Novu · Courier",
    ),
    "support": (
        "bring your own", "Support", "@byo-oss/support",
        "Tickets, contacts and agent replies inside your app.",
        "queue", [("#1042 Can't reset password", "open"), ("#1041 Invoice question", "solved")], "exit → Zendesk · Plain · Front",
    ),
    "entitlements": (
        "bring your own", "Entitlements", "@byo-oss/entitlements",
        "Plans, features, limits and usage from one typed catalog.",
        "acme · pro", [("requests · 940 / 1,000", "pro"), ("sso · upgrade to Team", "refused")], "exit → Autumn · Stigg · Schematic",
    ),
    "mailer": (
        "bring your own", "Mailer", "@byo-oss/mailer",
        "The email sender BYO packages share: Wraps, SES or email-sdk.",
        "outbox", [("→ alice@example.com", "sent"), ("wraps · ses · email-sdk", "adapter")], "exit → your provider's SDK",
    ),
    "core": (
        "bring your own", "Core", "@byo-oss/core",
        "One event bus, one cron route and one org-cleanup call for every BYO plugin.",
        "wiring", [("createEventBus([…])", "events"), ("sweepAll(auth)", "cron"), ("org deleted", "cleanup")], "no tables, no endpoints",
    ),
    "conventions": (
        "bring your own", "Conventions", "byo-oss/conventions",
        "The rules that let BYO packages work as one system on better-auth.",
        "SPEC.md", [("§9 exit path", "required"), ("§11 shared packages", "required")], "one identity · one permission model",
    ),
    "site": (
        "bring your own", "byo.dev", "byo-oss/site",
        "Product pages, docs and conventions for BYO packages.",
        "byo.dev", [("/docs/notifications", "docs"), ("/conventions", "spec")], "built from each package's docs",
    ),
}


def wordmark() -> str:
    svg = (DESIGN / "byo-wordmark.svg").read_text()
    return re.sub(r"<title>.*?</title>", "", svg)


def fill(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def shoot(page: Path, theme: str, size: tuple[int, int], out: Path, scale: int = SCALE) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "chromium", "--headless", "--disable-gpu", "--hide-scrollbars",
            "--no-sandbox", f"--force-device-scale-factor={scale}",
            f"--window-size={size[0]},{size[1]}", "--virtual-time-budget=3000",
            f"--screenshot={out}", f"file://{page}?theme={theme}",
        ],
        check=True, capture_output=True,
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        build = Path(tmp)
        for name in ("tokens.css",):
            (build / name).write_text((DESIGN / name).read_text())
        (build / "fonts").symlink_to(DESIGN / "fonts")

        for name, size in (("banner", (1280, 360)), ("diagram", (1120, 760))):
            page = build / f"{name}.html"
            page.write_text(fill((DESIGN / f"{name}.html").read_text(), {"WORDMARK": wordmark()}))
            stem = "how-it-fits" if name == "diagram" else name
            for theme in ("dark", "light"):
                shoot(page, theme, size, ROOT / "profile" / "assets" / f"{stem}-{theme}.png")

        template = (DESIGN / "social.html").read_text()
        for repo, (eyebrow, title, pkg, tagline, head, rows, exit_line) in SOCIAL.items():
            cells = "".join(
                f'<div class="row{" dim" if i else ""}"><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>'
                for i, (a, b) in enumerate(rows)
            )
            page = build / f"social-{repo}.html"
            page.write_text(fill(template, {
                "WORDMARK": wordmark(), "EYEBROW": html.escape(eyebrow), "TITLE": html.escape(title),
                "PKG": html.escape(pkg), "TAGLINE": html.escape(tagline), "HEAD": html.escape(head),
                "ROWS": cells, "EXIT": html.escape(exit_line),
            }))
            shoot(page, "dark", (1280, 640), ROOT / "social" / f"{repo}.png", scale=1)  # GitHub's 1280x640


if __name__ == "__main__":
    main()
