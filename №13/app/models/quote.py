from dataclasses import dataclass, field
from datetime import date


@dataclass
class Night:
    day: date          # дата, когда гость ложится спать (ночь с day на day + 1)
    price: int
    weekend: bool


@dataclass
class Quote:
    """Расчёт стоимости проживания."""
    nights: list = field(default_factory=list)
    subtotal: int = 0
    long_stay_percent: int = 0
    promo_code: str = ""
    promo_percent: int = 0
    total: int = 0

    def to_dict(self):
        return {
            "nights": [
                {"day": n.day.isoformat(), "price": n.price, "weekend": n.weekend}
                for n in self.nights
            ],
            "subtotal": self.subtotal,
            "long_stay_percent": self.long_stay_percent,
            "promo_code": self.promo_code,
            "promo_percent": self.promo_percent,
            "total": self.total,
        }
