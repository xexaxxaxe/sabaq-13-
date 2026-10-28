import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "urok-4-hotel-secret-key"
SESSION_COOKIE_NAME = "hotel_student"
DATABASE = os.path.join(BASE_DIR, "hotel.db")
PORT = 5000

# ---------- Заезд и выезд ----------
CHECKIN_HOUR = 14          # заезд с 14:00
CHECKOUT_HOUR = 12         # выезд до 12:00
MAX_NIGHTS = 30            # максимум ночей в одной брони
FREE_CANCEL_HOURS = 48     # бесплатная отмена — не позже чем за 48 часов до заезда

# ---------- Цены ----------
WEEKEND_EXTRA_PERCENT = 25     # наценка за ночь с пятницы на субботу и с субботы на воскресенье
INCLUDED_GUESTS = 2            # сколько гостей входит в цену номера
EXTRA_GUEST_FEE = 5000         # доплата за каждого гостя сверх INCLUDED_GUESTS, за ночь, ₸
LONG_STAY_NIGHTS = 7           # от скольких ночей действует скидка за долгое проживание
LONG_STAY_PERCENT = 10         # размер этой скидки

# Промокоды: код -> скидка в процентах (применяется после скидки за долгое проживание)
PROMO_CODES = {
    "STUDENT": 10,
    "OSEN2026": 15,
}
