def money(value):
    """45000 -> '45 000 ₸'."""
    return f"{value:,}".replace(",", " ") + " ₸"


def _plural(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return one
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return few
    return many


def nights_word(n):
    """3 -> '3 ночи'."""
    return f"{n} {_plural(n, 'ночь', 'ночи', 'ночей')}"


def guests_word(n):
    """2 -> '2 гостя'."""
    return f"{n} {_plural(n, 'гость', 'гостя', 'гостей')}"
