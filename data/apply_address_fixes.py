#!/usr/bin/env python3
"""Применяет вручную найденные реальные адреса (data/addresses_filled.csv) —
геокодирует их через Яндекс (для реальных адресов он очень точен) и патчит
locations_final_geocoded_merged.json. Новые id (не найденные в текущем датасете)
добавляются как новые места."""
import csv
import json
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV_PATH = ROOT / "data" / "addresses_filled.csv"
DATA_PATH = ROOT / "data" / "locations_final_geocoded_merged.json"
API_KEY = "b80ab8de-5c9d-419f-ba05-f0d3d2ce7891"

PAREN_SUFFIX = re.compile(r"\s*\([^)]*\)\s*$")


def geocode(query):
    url = "https://geocode-maps.yandex.ru/1.x/?" + urllib.parse.urlencode({
        "apikey": API_KEY, "geocode": query, "format": "json", "lang": "ru_RU", "results": 1,
    })
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
        members = data["response"]["GeoObjectCollection"]["featureMember"]
        if members:
            pos = members[0]["GeoObject"]["Point"]["pos"]
            lon, lat = map(float, pos.split())
            return lat, lon
    except Exception as e:
        print("  ERR", query, e)
    return None


def geocode_with_fallback(address):
    res = geocode(address)
    if res:
        return res, "exact"
    stripped = PAREN_SUFFIX.sub("", address).strip()
    if stripped != address:
        res = geocode(stripped)
        if res:
            return res, "exact"
    return None, "city_fallback"


def main():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8-sig")))
    rows = [r for r in rows if r.get("id")]

    items = json.load(open(DATA_PATH, encoding="utf-8"))
    by_id = {i["id"]: i for i in items}
    max_id = max(i["id"] for i in items)

    updated, added, failed = 0, 0, []

    for i, row in enumerate(rows):
        rid = int(row["id"])
        name = row["название"]
        city = row["город"]
        address = row["адрес (заполнить)"].strip()

        coords, precision = geocode_with_fallback(address)
        print(f"[{i+1}/{len(rows)}] #{rid} {name} -> {coords} [{precision}]")

        if not coords:
            failed.append((rid, name, address))
            time.sleep(0.15)
            continue

        if rid in by_id:
            by_id[rid]["lat"], by_id[rid]["lng"] = coords
            by_id[rid]["geo_precision"] = "exact"
            by_id[rid]["address"] = address
            updated += 1
        else:
            # новое место (например, разбитые на конкретные варианты "roomroom")
            new_item = {
                "id": rid,
                "name": name,
                "city": city,
                "cat": "stay" if "room" in name.lower() else "city",
                "lat": coords[0], "lng": coords[1],
                "teaser": name,
                "desc": name,
                "tags": [],
                "photos": [],
                "geo_precision": "exact",
                "address": address,
            }
            items.append(new_item)
            by_id[rid] = new_item
            added += 1

        time.sleep(0.15)

    # общий "roomroom" заменён в CSV на 4 конкретных варианта - убираем старый дубль
    has_specific_roomroom = any(i["name"].startswith("roomroom") and i["name"] != "roomroom" for i in items)
    if has_specific_roomroom:
        before = len(items)
        items = [i for i in items if i["name"] != "roomroom"]
        if len(items) != before:
            print(f"Убран дублирующий общий 'roomroom' (заменён на конкретные варианты)")

    json.dump(items, open(DATA_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nОбновлено: {updated}, добавлено новых: {added}, не удалось геокодировать: {len(failed)}")
    for rid, name, addr in failed:
        print("  НЕ НАЙДЕНО:", rid, name, addr)
    print(f"Итого мест: {len(items)} -> {DATA_PATH}")


if __name__ == "__main__":
    main()
