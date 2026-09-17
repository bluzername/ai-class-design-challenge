#!/usr/bin/env python3
"""Static checks for index.html: well-formed structure, numbered slides, pinned CDN assets."""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DECK = Path(__file__).resolve().parent.parent / "index.html"
UNPINNED_CDN = re.compile(r'cdn\.jsdelivr\.net/npm/[^"\s]+@\d+"')


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.in_title = False
        self.slides: list[int] = []
        self.scripts: list[str] = []
        self.insecure: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "div" and "slide" in (attr.get("class") or "").split() and attr.get("data-slide"):
            self.slides.append(int(attr["data-slide"]))
        if tag == "script" and attr.get("src"):
            self.scripts.append(attr["src"])
        for value in attr.values():
            if value and value.startswith("http://"):
                self.insecure.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def check(source: str) -> list[str]:
    parser = DeckParser()
    parser.feed(source)
    problems: list[str] = []
    title = "".join(parser.title_parts).strip()
    if not title:
        problems.append("missing <title>")
    if not parser.slides:
        problems.append("no .slide elements with data-slide found")
    elif parser.slides != list(range(1, len(parser.slides) + 1)):
        problems.append(f"slides are not numbered 1..N in order: {parser.slides}")
    for src in parser.scripts:
        if UNPINNED_CDN.search(f'{src}"'):
            problems.append(f"CDN script is not pinned to an exact version: {src}")
    for url in parser.insecure:
        problems.append(f"insecure http:// asset: {url}")
    return problems


def main() -> int:
    source = DECK.read_text(encoding="utf-8")
    problems = check(source)
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    print(f"OK: {DECK.name} has a title and correctly numbered slides; CDN assets are pinned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
