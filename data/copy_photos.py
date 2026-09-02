#!/usr/bin/env python3
"""Копирует только те фото из архива, что реально используются в карте, в images/,
переименовывая по id места, и уменьшает через sips (macOS) для веба."""
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARCHIVE = ROOT / "Telegram Desktop" / "ChatExport_2026-06-26"
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

loc = json.load(open(ROOT / "data" / "locations_final_geocoded_merged.json", encoding="utf-8"))

copied = {}
for item in loc:
    photos = item.get("photos") or []
    if not photos:
        continue
    src = ARCHIVE / photos[0]
    if not src.exists():
        continue
    if photos[0] not in copied:
        dest_name = f"{item['id']}.jpg"
        dest = IMAGES_DIR / dest_name
        shutil.copy2(src, dest)
        subprocess.run(
            ["sips", "-Z", "900", "-s", "formatOptions", "80", str(dest)],
            capture_output=True,
        )
        copied[photos[0]] = dest_name
    item["photo"] = copied[photos[0]]

json.dump(loc, open(ROOT / "data" / "locations_final_geocoded_merged.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"Скопировано уникальных фото: {len(copied)}, привязано к местам: {sum(1 for i in loc if i.get('photo'))}/{len(loc)}")
