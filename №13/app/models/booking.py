from dataclasses import dataclass
from datetime import date


@dataclass
class Booking:
    id: int
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int
    total: int
    promo: str
    status: str
    created: str

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    @property
    def is_confirmed(self):
        return self.status == "confirmed"

    def overlaps(self, check_in, check_out):
        """Пересекается ли эта бронь с проживанием с check_in по check_out."""
        return self.check_in < check_out and check_in < self.check_out
