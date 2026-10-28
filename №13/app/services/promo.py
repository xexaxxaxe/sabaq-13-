"""Промокоды."""
import config


class PromoError(Exception):
    pass


def normalize(code):
    return (code or "").strip().upper()


def promo_percent(code):
    """Скидка по промокоду в процентах. Пустой код — 0 %."""
    code = normalize(code)
    if not code:
        return 0
    if code not in config.PROMO_CODES:
        raise PromoError(f"Промокод «{code}» не найден")
    return config.PROMO_CODES[code]
