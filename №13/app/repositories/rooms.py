from ..db import get_db
from ..models import Room
from . import queries


def _to_room(row):
    return Room(
        id=row["id"],
        number=row["number"],
        floor=row["floor"],
        type_name=row["type_name"],
        price=row["price"],
        capacity=row["capacity"],
        description=row["description"],
    )


def all_rooms():
    return [_to_room(r) for r in get_db().execute(queries.ALL_ROOMS).fetchall()]


def get(room_id):
    row = get_db().execute(queries.ROOM_BY_ID, (room_id,)).fetchone()
    return _to_room(row) if row else None
