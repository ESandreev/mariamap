#!/usr/bin/env python3
"""Готовит партии мест, для которых ещё нет скачанного фото, под запуск
сабагентов. Смотрит, что уже лежит в photo_batches/downloaded/*/{id}.jpg,
и разбивает оставшееся на партии заданного размера.

Использование: python3 prepare_remaining_batches.py [размер_партии=8]
Результат: data/photo_batches/remaining/batch_NN.json
"""
import json
import glob
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BATCH_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 8

loc = json.load(open(ROOT / "locations_final_geocoded_merged.json", encoding="utf-8"))
simple = [
    {"id": l["id"], "name": l["name"], "city": l["city"], "cat": l["cat"],
     "lat": l["lat"], "lng": l["lng"], "current_photo": l.get("photo")}
    for l in loc
]

done_ids = set()
for f in glob.glob(str(ROOT / "photo_batches" / "downloaded" / "batch_*" / "*.jpg")):
    base = os.path.basename(f).replace(".jpg", "")
    if base.isdigit():
        done_ids.add(int(base))

remaining = [it for it in simple if it["id"] not in done_ids]
print(f"Всего мест: {len(simple)}, уже с фото: {len(done_ids)}, осталось: {len(remaining)}")

out_dir = ROOT / "photo_batches" / "remaining"
out_dir.mkdir(exist_ok=True)
for f in out_dir.glob("batch_*.json"):
    f.unlink()

chunks = [remaining[i:i + BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
for idx, ch in enumerate(chunks):
    json.dump(ch, open(out_dir / f"batch_{idx+1:02d}.json", "w", encoding="utf-8"),
               ensure_ascii=False, indent=2)
    (ROOT / "photo_batches" / "downloaded" / f"remaining_batch_{idx+1:02d}").mkdir(
        parents=True, exist_ok=True)

print(f"Готово: {len(chunks)} партий по {BATCH_SIZE} мест в data/photo_batches/remaining/")
print(f"Папки для скачивания уже созданы: data/photo_batches/downloaded/remaining_batch_01/ .. remaining_batch_{len(chunks):02d}/")
