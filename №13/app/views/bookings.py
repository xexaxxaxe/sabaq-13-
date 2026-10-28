from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from ..auth import login_required
from ..repositories import bookings as bookings_repo
from ..repositories import rooms as rooms_repo
from ..services import booking, promo
from ..utils import validators

bp = Blueprint("bookings", __name__)


@bp.route("/book/<int:room_id>", methods=["POST"])
@login_required
def book(room_id):
    room = rooms_repo.get(room_id)
    if room is None:
        abort(404)
    back = url_for(
        "rooms.room_page",
        room_id=room.id,
        check_in=request.form.get("check_in", ""),
        check_out=request.form.get("check_out", ""),
        guests=request.form.get("guests", ""),
    )
    try:
        check_in, check_out = validators.parse_period(
            request.form.get("check_in"), request.form.get("check_out")
        )
        guests = validators.parse_guests(request.form.get("guests"), room.capacity)
        booking_id = booking.create(
            session["user_id"], room, check_in, check_out, guests, request.form.get("promo", "")
        )
    except (validators.ValidationError, promo.PromoError, booking.BookingError) as e:
        flash(str(e))
        return redirect(back)

    flash(f"Бронь №{booking_id} подтверждена. Ждём вас!")
    return redirect(url_for("bookings.my_bookings"))


@bp.route("/bookings")
@login_required
def my_bookings():
    items = []
    for b in bookings_repo.for_user(session["user_id"]):
        items.append({
            "booking": b,
            "room": rooms_repo.get(b.room_id),
            "can_cancel": booking.can_cancel(b),
            "deadline": booking.cancel_deadline(b),
        })
    return render_template("bookings.html", items=items)


@bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel(booking_id):
    try:
        booking.cancel(session["user_id"], booking_id)
    except booking.BookingError as e:
        flash(str(e))
    else:
        flash(f"Бронь №{booking_id} отменена")
    return redirect(url_for("bookings.my_bookings"))
