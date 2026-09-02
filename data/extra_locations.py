#!/usr/bin/env python3
"""Места вне рубрики #картапутешествий: гайды по ресторанам Москвы и личные
отзывы о разовых визитах, тоже найденные в архиве канала. Пишет extra_locations.json."""
import json
from pathlib import Path

POSTS_PATH = Path(__file__).parent / "posts.json"
OUT_PATH = Path(__file__).parent / "extra_locations.json"

posts = {p["id"]: p for p in json.load(open(POSTS_PATH, encoding="utf-8"))}


def photos_of(*ids):
    out = []
    for i in ids:
        out += posts.get(i, {}).get("photos", [])
    return out


EXTRA = [
    # --- Гайд по японским ресторанам Москвы (message954) ---
    dict(city="Москва", name="AYU", cat="food", section="food",
         desc="Классический японский суси-омакасе ресторан в японском дворике WA Garden.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="UCHIWA", cat="food", section="food",
         desc="Кайсэки-ресторан о деликатесах Японии, в японском дворике WA Garden.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="TAJIRI GO", cat="food", section="food",
         desc="Мраморную говядину вагю готовят на японских грилях, формат омакасе.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Jun", cat="food", section="food",
         desc="Считается, что тут самые правильные и вкусные суши в Москве.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Hibiki", cat="food", section="food",
         desc="Ресторан современной японской кухни. Дорого, но своих денег стоит.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Amber", cat="food", section="food",
         desc="Raw bar, открытая кухня и лучший вид на закаты Цветного бульвара. Хорошее место для свидания.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Self Edge Japanese", cat="food", section="food",
         desc="Для любителей красивых тарелочек — большая коллекция фарфора прямиком из Европы. Вкусная современная японская кухня.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954", "message951")),
    dict(city="Москва", name="Fullmoon", cat="food", section="food",
         desc="Японская кухня, бар и чайная комната. Два зала, противоположных по стилистике.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Hachiko", cat="food", section="food",
         desc="Больше классических и знакомых позиций, но есть и блюда традиционной японской кухни. Дог-френдли.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Tottori", cat="food", section="food",
         desc="Сюда идём за вкусным раменом. 14 видов рамена, вагю и саке.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Tabi", cat="food", section="food",
         desc="Формат андеграундного аудио-бара от создателя Black Swan, Дениса Бобкова — умеет создавать правильную атмосферу.",
         source_post="message954", source_date="05.11.2025", photos=photos_of("message954")),
    dict(city="Москва", name="Ikura Izakaya Nikkei", cat="food", section="food",
         desc="Единственный в Москве ресторан перуано-японской кухни. Классические японские блюда с яркими перуанскими соусами, техника приготовления на открытом огне.",
         source_post="message488", source_date="13.04.2025", photos=photos_of("message488")),

    # --- Гайд по греческим ресторанам Москвы (message1070) ---
    dict(city="Москва", name="Pafos", cat="food", section="food",
         desc="Греческое шоу с танцами, песнями и битьём тарелок — атмосфера греческих курортов.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),
    dict(city="Москва", name="Eva", cat="food", section="food",
         desc="Ресторан современной греческой кухни. Акцент на мезе, дипах и блюдах на открытом огне и в печи.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070", "message1062")),
    dict(city="Москва", name="The Greeks", cat="food", section="food",
         desc="Средиземноморский ресторан Антона Пинского.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),
    dict(city="Москва", name="Meraki", cat="food", section="food",
         desc="Ресторан повседневной греческой кухни от Аркадия Новикова.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),
    dict(city="Москва", name="Papandopulo", cat="food", section="food",
         desc="Новый молодёжный ресторан. Говорят, тут лучший гирос в городе.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),
    dict(city="Москва", name="Kefi", cat="food", section="food",
         desc="Совладелец — грек по национальности, меню максимально приближено к греческой классике. Музыкальные вечера с игрой на традиционных инструментах.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),
    dict(city="Москва", name="Molon Lave", cat="food", section="food",
         desc="Простой интерьер, но ресторану уже больше 11 лет — знак качества. Есть собственная лавка продуктов из Греции.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),
    dict(city="Москва", name="Кухня Кипра", cat="food", section="food",
         desc="Греческий фастфуд. Есть в Авиапарке, ТЦ Цветной и на Даниловском рынке.",
         source_post="message1070", source_date="26.01.2026", photos=photos_of("message1070")),

    # --- Топ-5 виноделен Краснодарского края (message1212) ---
    dict(city="Краснодарский край", name="Шато де Талю", cat="nature", section="activity",
         desc="Самая эффектная винодельня Геленджика, атмосфера французского шато на берегу Чёрного моря. Стоит приезжать на закат, гулять по территории, смотреть на бухту с высоты и ужинать с видом на виноградники.",
         source_post="message1212", source_date="18.06.2026", photos=photos_of("message1212")),
    dict(city="Краснодарский край", name="Имение Сикоры", cat="nature", section="activity",
         desc="Семейная винодельня с мировым рейтингом — одна из самых современных как по архитектуре, так и по процессу производства вина.",
         source_post="message1212", source_date="18.06.2026", photos=photos_of("message1212")),
    dict(city="Краснодарский край", name="Скалистый берег", cat="nature", section="activity",
         desc="Больше похоже на музей современного искусства, чем на винодельню. Здание в стиле бионической архитектуры, как гигантская морская галька над склоном.",
         source_post="message1212", source_date="18.06.2026", photos=photos_of("message1212")),
    dict(city="Краснодарский край", name="Гай-Кодзор", cat="nature", section="activity",
         desc="Современное здание, встроенное в ландшафт Анапской долины, с панорамными видами на виноградники и горы.",
         source_post="message1212", source_date="18.06.2026", photos=photos_of("message1212")),
    dict(city="Краснодарский край", name="Долина Лефкадия", cat="nature", section="activity",
         desc="Настоящая винная долина с виноградниками, лавандовыми полями, сыроварней, ресторанами и атмосферой европейского загородного путешествия.",
         source_post="message1212", source_date="18.06.2026", photos=photos_of("message1212")),

    # --- Личные отзывы о разовых визитах ---
    dict(city="Иркутск", name="Белая ворона", cat="cafe", section="food",
         desc="Кофейня и сувенирная лавка семейного проекта. Керамика, открытки, свечи, украшения — всё сделано местными мастерами вручную. Никаких стандартных сувениров.",
         source_post="message189", source_date="30.05.2023", photos=photos_of("message133", "message189")),
    dict(city="Москва", name="La Bottega Siciliana", cat="food", section="food",
         desc="Итальянский ресторан, специализируется на сицилийской кухне. Бренд-шеф Нино Грациано — две звезды Мишлен за ресторан в Сицилии. Тут самая вкусная пицца в Москве (по мнению многих) и отличный баклажан по рецепту шефа.",
         source_post="message996", source_date="30.11.2025", photos=photos_of("message996")),
    dict(city="Москва", name="Olluco", cat="food", section="food",
         desc="Проект Вирхилио Мартинеса, одного из самых титулованных шеф-поваров планеты (его ресторан Central в Перу — 4-е место в рейтинге 50 лучших ресторанов мира). Исследует традиционные вкусы разных территорий — за один визит словно отправляешься в гастрономическое путешествие.",
         source_post="message1034", source_date="26.12.2025", photos=photos_of("message1033", "message1034")),
    dict(city="Москва", name="Savoy", cat="food", section="food",
         desc="Ресторан в центре Москвы с более чем 100-летней историей, пережил революцию, сохранил исторические интерьеры. После долгой реконструкции открылся заново.",
         source_post="message920", source_date="16.10.2025", photos=photos_of("message920")),
    dict(city="Москва", name="Sangre Fresca", cat="food", section="food",
         desc="Мексиканский ресторан. Лучшая Bloody Mary в городе (в том числе безалкогольная версия), хороший выбор закусок. Тако не впечатлили — но если любите острое, понравится.",
         source_post="message1096", source_date="09.02.2026", photos=photos_of("message1096")),
    dict(city="Ожигово (Московская область)", name="На Даче", cat="food", section="food",
         desc="Загородный гастропроект бренд-шефа Дмитрия Парикова — chef's table на его дачном участке, в часе езды от центра Москвы. Встреча на вокзале, электричка, шеф с настойками на перроне, ужин на даче с песнями у костра.",
         source_post="message756", source_date="17.07.2025", photos=photos_of("message756")),
    dict(city="под Санкт-Петербургом", name="WeLodge", cat="stay", section="stay",
         desc="Загородный отель на берегу озера, дизайн вдохновлён африканскими лоджами в стиле сафари. Деревянные дома из массивного бруса, камины, SPA-зона с панорамными окнами. На территории 2 ресторана, по выходным — ужин с шеф-поваром на открытом огне.",
         source_post="message1017", source_date="13.12.2025", photos=photos_of("message1017")),
    dict(city="Суздаль", name="Дымов Дача", cat="stay", section="stay",
         desc="6 гостевых домов в центре Суздаля, отреставрированных семьёй Дымовых из ветхих исторических зданий. Можно с животными любого размера. Стоит заказать чаепитие из самовара с ватрушками и рогаликами.",
         source_post="message1132", source_date="05.03.2026", photos=photos_of("message1132")),
]


def main():
    json.dump(EXTRA, open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(EXTRA)} дополнительных мест -> {OUT_PATH}")


if __name__ == "__main__":
    main()
