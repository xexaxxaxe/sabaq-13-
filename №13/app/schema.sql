CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS room_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,          -- цена за ночь, ₸
    capacity INTEGER NOT NULL,       -- максимум гостей
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT UNIQUE NOT NULL,
    type_id INTEGER NOT NULL REFERENCES room_types (id),
    floor INTEGER NOT NULL
);

-- даты хранятся как 'ГГГГ-ММ-ДД'; check_out — день выезда (эта ночь уже не оплачивается)
-- status: 'confirmed' — подтверждена, 'cancelled' — отменена
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users (id),
    room_id INTEGER NOT NULL REFERENCES rooms (id),
    check_in TEXT NOT NULL,
    check_out TEXT NOT NULL,
    guests INTEGER NOT NULL,
    total INTEGER NOT NULL,
    promo TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'confirmed',
    created TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
