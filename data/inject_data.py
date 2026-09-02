#!/usr/bin/env python3
"""Вставляет собранный LOCATIONS-массив в index.html вместо демо-данных."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "data" / "locations_final_geocoded_merged.json"
INDEX_PATH = ROOT / "index.html"

items = json.load(open(DATA_PATH, encoding="utf-8"))


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def js_item(i):
    photo = f', photo:{js_str(i["photo"])}' if i.get("photo") else ""
    tags = ", ".join(js_str(t) for t in i.get("tags", []))
    return (
        f'    {{ id:{i["id"]}, name:{js_str(i["name"])}, city:{js_str(i["city"])}, '
        f'cat:{js_str(i["cat"])}, lat:{i["lat"]}, lng:{i["lng"]},\n'
        f'      teaser:{js_str(i["teaser"])},\n'
        f'      desc:{js_str(i["desc"])},\n'
        f'      tags:[{tags}]{photo} }}'
    )


body = ",\n".join(js_item(i) for i in items)
new_block = (
    "  const LOCATIONS = [\n"
    f"{body}\n"
    "  ];"
)

html = INDEX_PATH.read_text(encoding="utf-8")
pattern = re.compile(r"  const LOCATIONS = \[.*?\n  \];", re.S)
new_html, n = pattern.subn(new_block, html, count=1)
if n != 1:
    raise SystemExit("Не удалось найти блок LOCATIONS в index.html")

INDEX_PATH.write_text(new_html, encoding="utf-8")
print(f"Вставлено {len(items)} мест в {INDEX_PATH}")
