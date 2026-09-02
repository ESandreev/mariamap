#!/usr/bin/env python3
"""Геокодирует места из locations_final.json через Nominatim (OSM). Уважает лимит 1 req/sec."""
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

IN_PATH = Path(__file__).parent / "locations_final.json"
OUT_PATH = Path(__file__).parent / "locations_geocoded.json"
UA = "travel-map-blog-project/1.0 (personal travel blog map, one-time batch geocoding)"

CITY_QUERY = {
    "Суздаль": "Суздаль, Владимирская область, Россия",
    "Владимир": "Владимир, Россия",
    "Плёс": "Плёс, Ивановская область, Россия",
    "Коломна": "Коломна, Московская область, Россия",
    "Нижний Новгород": "Нижний Новгород, Россия",
    "Кострома": "Кострома, Россия",
    "Тула": "Тула, Россия",
    "Серпухов": "Серпухов, Московская область, Россия",
    "Поленово": "Поленово, Тульская область, Россия",
    "Таруса": "Таруса, Калужская область, Россия",
    "Ярославль": "Ярославль, Россия",
}


def geocode(query):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": query, "format": "json", "limit": 1, "countrycodes": "ru",
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print("  ERR", query, e)
    return None


def main():
    items = json.load(open(IN_PATH, encoding="utf-8"))

    # 1. Координаты городов (для fallback и для центрирования)
    city_coords = {}
    for city, q in CITY_QUERY.items():
        res = geocode(q)
        city_coords[city] = res
        print(f"город {city}: {res}")
        time.sleep(1.1)

    # 2. Каждое место: "Название, Город, Россия"
    for i, item in enumerate(items):
        city = item["city"]
        q = f"{item['name']}, {CITY_QUERY.get(city, city + ', Россия')}"
        res = geocode(q)
        if res:
            item["lat"], item["lng"] = res
            item["geo_precision"] = "exact"
        else:
            fallback = city_coords.get(city)
            if fallback:
                item["lat"], item["lng"] = fallback
            item["geo_precision"] = "city_fallback"
        print(f"[{i+1}/{len(items)}] {item['name']} ({city}) -> {item.get('lat')},{item.get('lng')} [{item['geo_precision']}]")
        time.sleep(1.1)

    json.dump(items, open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    exact = sum(1 for i in items if i["geo_precision"] == "exact")
    print(f"\nГотово: {exact}/{len(items)} с точным геокодингом -> {OUT_PATH}")


if __name__ == "__main__":
    main()
