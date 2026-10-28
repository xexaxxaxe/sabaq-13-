"""Начальные данные: типы номеров и сами номера."""

ROOM_TYPES = [
    ("Стандарт", 15000, 2, "Уютный номер с видом на сосновый лес. Двуспальная кровать."),
    ("Комфорт", 22000, 3, "Просторный номер с балконом. Двуспальная кровать и диван."),
    ("Семейный", 30000, 4, "Две комнаты, две кровати и диван. Подойдёт для семьи с детьми."),
    ("Люкс", 45000, 2, "Панорамные окна на горы, камин и большая ванна."),
]

# (номер, id типа, этаж)
ROOMS = [
    ("101", 1, 1),
    ("102", 1, 1),
    ("103", 1, 1),
    ("201", 2, 2),
    ("202", 2, 2),
    ("203", 3, 2),
    ("301", 3, 3),
    ("302", 4, 3),
]


def fill(db):
    if db.execute("SELECT COUNT(*) FROM room_types").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO room_types (name, price, capacity, description) VALUES (?, ?, ?, ?)",
            ROOM_TYPES,
        )
    if db.execute("SELECT COUNT(*) FROM rooms").fetchone()[0] == 0:
        db.executemany("INSERT INTO rooms (number, type_id, floor) VALUES (?, ?, ?)", ROOMS)
