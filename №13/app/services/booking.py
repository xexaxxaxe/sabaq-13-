"""Создание и отмена броней."""
from datetime import datetime, timedelta

import config

from ..repositories import bookings as bookings_repo
from . import availability, pricing


class BookingError(Exception):
    pass


def create(user_id, room, check_in, check_out, guests, promo_code):
    """Даты и гости уже проверены (utils/validators.py). Возвращает id брони."""
    q = pricing.quote(room, check_in, check_out, guests, promo_code)

    bookings_repo.begin()
    try:
        if not availability.is_free(room.id, check_in, check_out):
            raise BookingError("На эти даты номер уже занят — выберите другие даты")
        booking_id = bookings_repo.create(
            user_id, room.id, check_in, check_out, guests, q.total, q.promo_code
        )
    except Exception:
        bookings_repo.rollback()
        raise
    bookings_repo.commit()
    return booking_id


def cancel_deadline(booking):
    """До какого момента бронь можно отменить бесплатно."""
    checkin_moment = datetime(
        booking.check_in.year,
        booking.check_in.month,
        booking.check_in.day,
        config.CHECKIN_HOUR,
    )
    return checkin_moment - timedelta(hours=config.FREE_CANCEL_HOURS)


def can_cancel(booking):
    return booking.is_confirmed and datetime.now() < cancel_deadline(booking)


def cancel(user_id, booking_id):
    booking = bookings_repo.get(booking_id, user_id)
    if booking is None:
        raise BookingError("Бронь не найдена")
    if not booking.is_confirmed:
        raise BookingError("Эта бронь уже отменена")
    if not can_cancel(booking):
        raise BookingError(
            f"Бесплатно отменить можно не позже чем за {config.FREE_CANCEL_HOURS} часов до заезда"
        )
    bookings_repo.cancel(booking_id)
