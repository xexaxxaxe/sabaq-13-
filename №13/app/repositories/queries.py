"""Все SQL-запросы приложения в одном месте."""

_ROOM_COLUMNS = """
SELECT r.id, r.number, r.floor,
       t.name AS type_name, t.price, t.capacity, t.description
FROM rooms r
JOIN room_types t ON t.id = r.type_id
"""

ALL_ROOMS = _ROOM_COLUMNS + "ORDER BY r.number"

ROOM_BY_ID = _ROOM_COLUMNS + "WHERE r.id = ?"

BOOKINGS_FOR_ROOM = """
SELECT * FROM bookings
WHERE room_id = ? AND status = 'confirmed'
ORDER BY check_in
"""

BOOKINGS_BY_USER = "SELECT * FROM bookings WHERE user_id = ? ORDER BY check_in DESC, id DESC"

BOOKING_BY_ID = "SELECT * FROM bookings WHERE id = ? AND user_id = ?"

INSERT_BOOKING = """
INSERT INTO bookings (user_id, room_id, check_in, check_out, guests, total, promo)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

CANCEL_BOOKING = "UPDATE bookings SET status = 'cancelled' WHERE id = ?"
