#!/usr/bin/env python3
"""Собирает locations_geocoded.json + extra_locations_geocoded.json в единый
LOCATIONS-массив для index.html. Разводит совпадающие city_fallback координаты
небольшим случайным сдвигом, чтобы маркеры не лежали друг на друге."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_PATH = ROOT / "data" / "locations_final_geocoded_merged.json"

random.seed(42)


def make_teaser(desc, name):
    if not desc:
        return name
    first = desc.split(". ")[0].strip()
    if not first.endswith((".", "!", "?", "…")):
        first += "."
    if len(first) > 140:
        first = first[:137].rsplit(" ", 1)[0] + "…"
    return first


def main():
    geo = json.load(open(ROOT / "data" / "locations_geocoded.json", encoding="utf-8"))
    extra = json.load(open(ROOT / "data" / "extra_locations_geocoded.json", encoding="utf-8"))
    all_items = geo + extra

    # разводим повторяющиеся city_fallback координаты небольшим джиттером (~300-600м)
    seen_coords = {}
    out = []
    for i, item in enumerate(all_items):
        lat, lng = item.get("lat"), item.get("lng")
        if lat is None or lng is None:
            continue  # без координат на карту не поставить
        key = (round(lat, 5), round(lng, 5))
        if item.get("geo_precision") == "city_fallback":
            n = seen_coords.get(key, 0)
            if n > 0:
                angle = random.uniform(0, 6.283)
                r = 0.004 * (1 + n // 8) * random.uniform(0.5, 1.0)
                lat += r * (0.6 + 0.4 * random.random()) * (1 if n % 2 == 0 else -1) * abs(__import__("math").cos(angle))
                lng += r * (1 if (n // 2) % 2 == 0 else -1) * abs(__import__("math").sin(angle))
            seen_coords[key] = n + 1

        out.append({
            "id": i + 1,
            "name": item["name"],
            "city": item["city"],
            "cat": item["cat"],
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "teaser": make_teaser(item["desc"], item["name"]),
            "desc": item["desc"] or item["name"],
            "tags": [],
            "photos": item.get("photos", []),
            "geo_precision": item.get("geo_precision"),
        })

    json.dump(out, open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    exact = sum(1 for i in out if i["geo_precision"] == "exact")
    print(f"Итого мест: {len(out)}, точных координат: {exact}, по центру города: {len(out)-exact}")
    print(f"-> {OUT_PATH}")


if __name__ == "__main__":
    main()
