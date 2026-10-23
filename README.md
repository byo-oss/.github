# byo-oss/.github

Organization profile for [github.com/byo-oss](https://github.com/byo-oss). GitHub renders `profile/README.md` on the org page.

| Path | What |
|---|---|
| `profile/README.md` | The org landing page |
| `profile/assets/` | Banner and "how they fit" diagram, light and dark, plus the org avatar |
| `social/` | 1280x640 social previews, one per repo. GitHub has no API for these: upload each under the repo's Settings > Social preview |
| `design/` | HTML sources for every image, with fonts and tokens copied from byo.dev |
| `scripts/build.py` | Renders `design/` to PNG with headless Chromium: `python3 scripts/build.py` |

Images are PNGs because GitHub renders SVG inside `<img>` without web fonts.

When a package's tagline or exit targets change, update `design/banner.html`, `design/diagram.html` and `scripts/build.py` together with `byo-site/src/data/site.ts`, then rebuild.
