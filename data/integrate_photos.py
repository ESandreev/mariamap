#!/usr/bin/env python3
"""Забирает скачанные сабагентами фото из photo_batches/downloaded/*/{id}.jpg,
пересжимает под формат сайта (как copy_photos.py), кладёт в images/{id}.jpg
и переключает поле photo:"..." у нужной записи в LOCATIONS внутри index.html.

Использование:
  python3 integrate_photos.py            # применить все найденные фото
  python3 integrate_photos.py --dry-run  # только показать, что было бы сделано
"""
import glob
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEX = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
DRY_RUN = "--dry-run" in sys.argv

files = sorted(glob.glob(str(ROOT / "data" / "photo_batches" / "downloaded" / "*" / "*.jpg")))
by_id = {}
for f in files:
    base = os.path.basename(f).replace(".jpg", "")
    if not base.isdigit():
        print(f"  пропуск (не число в имени файла): {f}")
        continue
    by_id[int(base)] = f

print(f"Найдено скачанных фото: {len(by_id)}")

content = INDEX.read_text(encoding="utf-8")
applied, missing = [], []

for loc_id, src_path in sorted(by_id.items()):
    pattern = re.compile(r'(\{\s*id:' + str(loc_id) + r',[\s\S]*?)photo:"[^"]*"(\s*\},)')
    m = pattern.search(content)
    if not m:
        missing.append(loc_id)
        continue
    dest_name = f"{loc_id}.jpg"
    applied.append((loc_id, dest_name))
    if not DRY_RUN:
        dest = IMAGES_DIR / dest_name
        subprocess.run(["sips", "-Z", "900", str(src_path), "--out", str(dest)],
                        capture_output=True)
        subprocess.run(["sips", "-s", "formatOptions", "80", str(dest)],
                        capture_output=True)
        content = pattern.sub(lambda mm: mm.group(1) + f'photo:"{dest_name}"' + mm.group(2),
                                content, count=1)

if missing:
    print(f"ВНИМАНИЕ: не нашёл запись с таким id в index.html: {missing}")

print(f"{'[dry-run] ' if DRY_RUN else ''}Обновлено записей: {len(applied)}")
for loc_id, dest_name in applied:
    print(f"  id={loc_id} -> images/{dest_name}")

if not DRY_RUN and applied:
    INDEX.write_text(content, encoding="utf-8")
    print("\nindex.html обновлён. Дальше: посмотреть diff, проверить локально, закоммитить,")
    print("запушить и подтянуть на сервере (git pull в /var/www/mariamap).")
elif DRY_RUN:
    print("\nЭто был dry-run, ничего не изменено. Запусти без --dry-run, чтобы применить.")
