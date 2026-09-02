#!/usr/bin/env python3
"""Извлекает места из постов #картапутешествий (формат 🔸-списков) в data/locations_raw.json."""
import json
import re
from pathlib import Path

POSTS_PATH = Path(__file__).parent / "posts.json"
OUT_PATH = Path(__file__).parent / "locations_raw.json"

CITY_ORDER = [
    "Суздаль", "Владимир", "Плес", "Плёс", "Коломна", "Нижний Новгород",
    "Кострома", "Тула", "Серпухов", "Поленово", "Таруса", "Ярославль",
]

# Явные привязки поста к городу (когда в тексте города нет явно в первой строке)
POST_CITY = {
    "message342": "Суздаль", "message351": "Суздаль", "message360": "Суздаль",
    "message403": "Владимир", "message410": "Владимир",
    "message467": "Плёс", "message475": "Плёс", "message486": "Плёс",
    "message503": "Коломна", "message512": "Коломна", "message517": "Коломна", "message522": "Коломна",
    "message535": "Нижний Новгород", "message545": "Нижний Новгород", "message548": "Нижний Новгород",
    "message565": "Кострома", "message575": "Кострома",
    "message593": "Тула", "message594": "Тула",
    "message630": "Серпухов", "message636": "Серпухов",
    "message657": "Поленово", "message665": "Поленово", "message669": "Поленово",
    "message699": "Таруса", "message708": "Таруса",
    "message824": "Ярославль", "message829": "Ярославль", "message833": "Ярославль",
}

SECTION_PATTERNS = [
    (re.compile(r"где жить", re.I), "stay"),
    (re.compile(r"где ес[тч]ь", re.I), "food"),
    (re.compile(r"что делать", re.I), "activity"),
    (re.compile(r"что купить", re.I), "shop"),
]

NATURE_HINTS = re.compile(
    r"баня|спа|заповедник|парк\b|пляж|сплав|лес\b|рыбалк|ферм|озер|река|прогул|термы|купол|глэмпинг",
    re.I,
)
CAFE_HINTS = re.compile(r"кафе|кофейн|кофе|чайная|кондитер|десерт|мороженн|пирож|пекарн", re.I)


def detect_section(line, current):
    for pat, sec in SECTION_PATTERNS:
        if pat.search(line):
            return sec
    return current


def classify(section, name, desc):
    text = f"{name} {desc}"
    if section == "stay":
        return "stay"
    if section == "shop":
        return "city"
    if section == "food":
        return "cafe" if CAFE_HINTS.search(text) else "food"
    # activity
    if NATURE_HINTS.search(text):
        return "nature"
    return "city"


DASH_SPLIT = re.compile(r"^(.{1,60}?)\s+[—–-]\s+(.+)$")
GUILLEMET_SPLIT = re.compile(r'^(.{0,20}?«[^»]{1,40}»)\s+(\S.*)$')
QUOTE_SPLIT = re.compile(r'^(.{0,20}?"[^"]{1,40}")\s+(\S.*)$')


def split_name_desc(line):
    """Пытается разбить '🔸 Имя Описание' в одной строке на (имя, описание)."""
    for pat in (DASH_SPLIT, GUILLEMET_SPLIT, QUOTE_SPLIT):
        m = pat.match(line)
        if m:
            return m.group(1).strip(" .-–—"), m.group(2).strip()
    return None


def parse_post(post, city):
    lines = post["text"].split("\n")
    section = None
    items = []  # (section, name, [desc lines])
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        new_section = detect_section(line, section)
        if new_section != section:
            section = new_section
            # строка сама по себе может быть просто заголовком, но иногда
            # содержит и заголовок и хэштег/часть - не считаем её пунктом
            continue
        if line.startswith("🔸") or line.startswith("🔹"):
            name = line.lstrip("🔸🔹").strip()
            # цена (💰💰💰) сама по себе не является пунктом
            if not name or set(name) <= {"💰"}:
                continue
            split = split_name_desc(name)
            if split:
                items.append([section, split[0], [split[1]]])
            else:
                items.append([section, name, []])
        elif set(line) <= {"💰"}:
            continue
        else:
            if items and items[-1][0] == section:
                items[-1][2].append(line)
            # иначе строка вне списка (вводный абзац) - игнорируем

    out = []
    for section, name, desc_lines in items:
        desc = " ".join(desc_lines).strip()
        if not section:
            continue
        cat = classify(section, name, desc)
        out.append({
            "city": city,
            "name": name,
            "section": section,
            "cat": cat,
            "desc": desc,
            "source_post": post["id"],
            "source_date": post["date"],
            "photos": post["photos"],
        })
    return out


def main():
    posts = json.load(open(POSTS_PATH, encoding="utf-8"))
    by_id = {p["id"]: p for p in posts}

    all_items = []
    for pid, city in POST_CITY.items():
        post = by_id.get(pid)
        if not post:
            print("WARN: пост не найден", pid)
            continue
        items = parse_post(post, city)
        all_items.extend(items)
        print(f"{pid} ({city}): {len(items)} пунктов")

    json.dump(all_items, open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nИтого: {len(all_items)} мест -> {OUT_PATH}")


if __name__ == "__main__":
    main()
