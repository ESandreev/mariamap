#!/usr/bin/env python3
"""Геокодирует extra_locations.json (гайды по Москве, разовые визиты) тем же способом."""
import json
import time
from pathlib import Path
from geocode import geocode, CITY_QUERY

IN_PATH = Path(__file__).parent / "extra_locations.json"
OUT_PATH = Path(__file__).parent / "extra_locations_geocoded.json"

EXTRA_CITY_QUERY = {
    # "Москва, Россия" геокодируется в центроид административной границы
    # (с учётом присоединённой Новой Москвы) — это ~16 км южнее исторического
    # центра. Поэтому для fallback используем координаты Театральной площади.
    "Москва": None,
    "Иркутск": "Иркутск, Россия",
    "Краснодарский край": "Краснодарский край, Россия",
    "Ожигово (Московская область)": "Ожигово, Московская область, Россия",
    "под Санкт-Петербургом": "Санкт-Петербург, Россия",
    "Суздаль": CITY_QUERY["Суздаль"],
}
MOSCOW_CENTER = (55.7597, 37.6188)  # Театральная площадь

# Точные адреса — там, где геокодинг по одному названию не находит место
# или находит что-то другое (сеть/тёзка).
ADDRESS_OVERRIDES = {
    "Ikura Izakaya Nikkei": "Рождественский бульвар, 1, Москва, Россия",
    "Fullmoon": "Малая Никитская улица, 16/5, Москва, Россия",
    "The Greeks": "Неглинная улица, 15, Москва, Россия",
}

# Координаты, перепроверенные вручную через Яндекс.Геокодер — Nominatim по
# этому адресу путал номер дома (нашёл 21с1 вместо 1, ошибка ~450м).
LATLNG_OVERRIDES = {
    "Ikura Izakaya Nikkei": (55.766749, 37.624211),
}


def main():
    items = json.load(open(IN_PATH, encoding="utf-8"))
    city_coords = {"Москва": MOSCOW_CENTER}
    for city, q in EXTRA_CITY_QUERY.items():
        if q is None:
            continue
        res = geocode(q)
        city_coords[city] = res
        print(f"город {city}: {res}")
        time.sleep(1.1)

    for i, item in enumerate(items):
        city = item["city"]
        if item["name"] in ADDRESS_OVERRIDES:
            q = ADDRESS_OVERRIDES[item["name"]]
        else:
            q = f"{item['name']}, {EXTRA_CITY_QUERY.get(city) or (city + ', Россия')}"
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
    print(f"Готово -> {OUT_PATH}")


if __name__ == "__main__":
    main()
