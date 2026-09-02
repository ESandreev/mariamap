#!/usr/bin/env python3
"""Парсит Telegram Desktop export (messages.html + messages2.html) в data/posts.json."""
import re
import json
import html as html_lib
from pathlib import Path

EXPORT_DIR = Path(__file__).parent.parent / "Telegram Desktop" / "ChatExport_2026-06-26"
OUT_PATH = Path(__file__).parent / "posts.json"

MESSAGE_RE = re.compile(
    r'<div class="message (?:default|service)[^"]*"\s+id="([^"]+)">(.*?)</div>\s*</div>\s*(?=<div class="message |\Z)',
    re.S,
)
DATE_RE = re.compile(r'title="(\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})')
SERVICE_DATE_RE = re.compile(r'<div class="body details">\s*([^<]+?)\s*</div>')
TEXT_RE = re.compile(r'<div class="text">(.*?)</div>\s*(?:<span class="reactions"|</div>\s*</div>)', re.S)
FROM_NAME_RE = re.compile(r'<div class="from_name">\s*([^<]+?)\s*</div>')
PHOTO_RE = re.compile(r'href="(photos/[^"]+\.jpg)"')
REACTION_RE = re.compile(r'<span class="emoji">\s*([^<]+?)\s*</span>\s*<span class="count">\s*(\d+)\s*</span>')


def strip_tags(text):
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_lib.unescape(text)
    return text.strip()


def parse_file(path):
    raw = path.read_text(encoding="utf-8")
    # Разбиваем по границам <div class="message ...
    chunks = re.split(r'(?=<div class="message (?:default|service))', raw)
    posts = []
    last_date = None
    for chunk in chunks:
        m = re.match(r'<div class="message (default|service)[^"]*"\s+id="([^"]+)"', chunk)
        if not m:
            continue
        kind, msg_id = m.group(1), m.group(2)
        if kind == "service":
            dm = SERVICE_DATE_RE.search(chunk)
            if dm:
                last_date = dm.group(1).strip()
            continue

        dm = DATE_RE.search(chunk)
        date, time = (dm.group(1), dm.group(2)) if dm else (last_date, None)

        tm = TEXT_RE.search(chunk)
        text = strip_tags(tm.group(1)) if tm else ""

        fm = FROM_NAME_RE.search(chunk)
        author = fm.group(1) if fm else None

        photos = sorted(set(PHOTO_RE.findall(chunk)))
        reactions = {e.strip(): int(c) for e, c in REACTION_RE.findall(chunk)}

        if not text and not photos:
            continue

        posts.append({
            "id": msg_id,
            "date": date,
            "time": time,
            "author": author,
            "text": text,
            "photos": photos,
            "reactions": reactions,
        })
    return posts


def main():
    all_posts = []
    for fname in ["messages.html", "messages2.html"]:
        fpath = EXPORT_DIR / fname
        if fpath.exists():
            posts = parse_file(fpath)
            print(f"{fname}: {len(posts)} постов")
            all_posts.extend(posts)

    OUT_PATH.write_text(json.dumps(all_posts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Итого: {len(all_posts)} постов -> {OUT_PATH}")


if __name__ == "__main__":
    main()
