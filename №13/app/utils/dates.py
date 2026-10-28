from datetime import datetime, timedelta

WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]


def parse_date(text):
    """'2026-11-05' -> date. Бросает ValueError, если строка неправильная."""
    return datetime.strptime(text, "%Y-%m-%d").date()


def nights(check_in, check_out):
    """Список ночей проживания: даты с check_in до check_out (не включая день выезда)."""
    return [check_in + timedelta(days=i) for i in range((check_out - check_in).days)]


def is_weekend_night(day):
    """Выходная ли ночь, которая начинается в день day."""
    return day.weekday() in (4, 5)


def human_date(day):
    """date -> 'пт, 6 ноября'."""
    return f"{WEEKDAYS[day.weekday()]}, {day.day} {MONTHS[day.month - 1]}"
