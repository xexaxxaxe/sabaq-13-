"""Какие номера свободны на выбранные даты."""
from ..repositories import bookings as bookings_repo
from ..repositories import rooms as rooms_repo


def is_free(room_id, check_in, check_out):
    return not any(b.overlaps(check_in, check_out) for b in bookings_repo.for_room(room_id))


def free_rooms(check_in, check_out, guests):
    return [
        room
        for room in rooms_repo.all_rooms()
        if room.capacity >= guests and is_free(room.id, check_in, check_out)
    ]
