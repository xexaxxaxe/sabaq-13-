"""Проверка дат и числа гостей, которые прислал пользователь."""
from datetime import date

import config

from .dates import parse_date


class ValidationError(Exception):
    pass


def parse_period(check_in_text, check_out_text):
    try:
        check_in = parse_date(check_in_text or "")
        check_out = parse_date(check_out_text or "")
    except ValueError:
        raise ValidationError("Укажите даты заезда и выезда")

    if check_in < date.today():
        raise ValidationError("Дата заезда уже прошла")
    if check_out <= check_in:
        raise ValidationError("Дата выезда должна быть позже даты заезда")
    if (check_out - check_in).days > config.MAX_NIGHTS:
        raise ValidationError(f"Можно забронировать не больше {config.MAX_NIGHTS} ночей")
    return check_in, check_out


def parse_guests(text, capacity=None):
    try:
        guests = int(text)
    except (TypeError, ValueError):
        raise ValidationError("Укажите число гостей")
    if guests < 1:
        raise ValidationError("Гостей должно быть не меньше одного")
    if capacity is not None and guests > capacity:
        raise ValidationError(f"В этом номере могут жить не больше {capacity} гостей")
    return guests
