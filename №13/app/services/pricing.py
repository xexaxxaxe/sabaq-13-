"""Расчёт стоимости проживания. Все числа — в config.py."""
import config

from ..models import Night, Quote
from ..utils import dates
from . import discounts, promo


def quote(room, check_in, check_out, guests, promo_code=""):
    extra = max(0, guests - config.INCLUDED_GUESTS) * config.EXTRA_GUEST_FEE

    result = Quote()
    for day in dates.nights(check_in, check_out):
        price = room.price
        weekend = dates.is_weekend_night(day)
        if weekend:
            price = price * (100 + config.WEEKEND_EXTRA_PERCENT) // 100
        price += extra
        result.nights.append(Night(day=day, price=price, weekend=weekend))

    result.subtotal = sum(n.price for n in result.nights)
    result.long_stay_percent = discounts.long_stay_percent(len(result.nights))
    result.promo_code = promo.normalize(promo_code)
    result.promo_percent = promo.promo_percent(promo_code)

    total = result.subtotal * (100 - result.long_stay_percent) // 100
    total = total * (100 - result.promo_percent) // 100
    result.total = total
    return result
