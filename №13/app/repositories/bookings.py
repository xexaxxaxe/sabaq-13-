from ..db import get_db
from ..models import Booking
from ..utils.dates import parse_date
from . import queries


def _to_booking(row):
    return Booking(
        id=row["id"],
        user_id=row["user_id"],
        room_id=row["room_id"],
        check_in=parse_date(row["check_in"]),
        check_out=parse_date(row["check_out"]),
        guests=row["guests"],
        total=row["total"],
        promo=row["promo"],
        status=row["status"],
        created=row["created"],
    )


def for_room(room_id):
    rows = get_db().execute(queries.BOOKINGS_FOR_ROOM, (room_id,)).fetchall()
    return [_to_booking(r) for r in rows]


def for_user(user_id):
    rows = get_db().execute(queries.BOOKINGS_BY_USER, (user_id,)).fetchall()
    return [_to_booking(r) for r in rows]


def get(booking_id, user_id):
    row = get_db().execute(queries.BOOKING_BY_ID, (booking_id, user_id)).fetchone()
    return _to_booking(row) if row else None


def begin():
    """Начинает транзакцию: пока она идёт, никто другой не может записывать в базу."""
    get_db().execute("BEGIN IMMEDIATE")


def commit():
    get_db().commit()


def rollback():
    get_db().rollback()


def create(user_id, room_id, check_in, check_out, guests, total, promo):
    cursor = get_db().execute(
        queries.INSERT_BOOKING,
        (user_id, room_id, check_in.isoformat(), check_out.isoformat(), guests, total, promo),
    )
    return cursor.lastrowid


def cancel(booking_id):
    db = get_db()
    db.execute(queries.CANCEL_BOOKING, (booking_id,))
    db.commit()
