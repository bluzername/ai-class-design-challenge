# Design the Next AI Class

[![CI](https://github.com/bluzername/ai-class-design-challenge/actions/workflows/ci.yml/badge.svg)](https://github.com/bluzername/ai-class-design-challenge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An interactive slide deck for a student class design challenge: students propose the next AI class and the deck walks them through the brief, constraints and judging.

**Live deck:** https://bluzername.github.io/ai-class-design-challenge/

## How it works

The whole deck is one file, `index.html`. It uses Tailwind CSS (browser build, pinned to an exact version on jsDelivr) and Google Fonts; everything else is inline.

- Navigate with the arrow buttons, the dots at the bottom, the left and right arrow keys, the space bar, or by swiping on touch devices.
- Slides are `<div class="slide" data-slide="N">` blocks numbered from 1. Add a new slide by copying one of them and giving it the next number; the navigation, dots and counter pick it up automatically.
- Elements with the `reveal` class animate in when a slide becomes active; `.bar-fill` elements animate to their `data-width` percentage.

## Run locally

Open `index.html` in a browser. No build step. Fonts and Tailwind load from their CDNs, so an internet connection is needed the first time.

## Deploy

GitHub Pages serves the `main` branch. Every push to `main` redeploys the deck.

## Checks

`scripts/check_deck.py` parses `index.html` and fails if the title is missing, the slides are not numbered `1..N` in order, a CDN script is not pinned to an exact version, or any asset is loaded over plain `http://`. CI runs it on every push and pull request, confirms every external asset URL returns 200, and rejects em or en dashes in the repo's text files.

```bash
python3 scripts/check_deck.py
```

## License

MIT
