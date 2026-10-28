from datetime import date, timedelta

from flask import Blueprint, abort, jsonify, render_template, request

import config

from ..repositories import rooms as rooms_repo
from ..services import availability, pricing, promo
from ..utils import validators

bp = Blueprint("rooms", __name__)


@bp.route("/room/<int:room_id>")
def room_page(room_id):
    room = rooms_repo.get(room_id)
    if room is None:
        abort(404)
    tomorrow = date.today() + timedelta(days=1)
    form = {
        "check_in": request.args.get("check_in", tomorrow.isoformat()),
        "check_out": request.args.get("check_out", (tomorrow + timedelta(days=2)).isoformat()),
        "guests": request.args.get("guests", str(min(2, room.capacity))),
    }
    return render_template(
        "room.html",
        room=room,
        form=form,
        today=date.today().isoformat(),
        cfg=config,
    )


@bp.route("/api/quote")
def api_quote():
    """Предварительный расчёт цены для формы бронирования (его вызывает quote.js)."""
    room = rooms_repo.get(request.args.get("room", type=int))
    if room is None:
        return jsonify({"error": "Номер не найден"}), 404
    try:
        check_in, check_out = validators.parse_period(
            request.args.get("check_in"), request.args.get("check_out")
        )
        guests = validators.parse_guests(request.args.get("guests"), room.capacity)
        q = pricing.quote(room, check_in, check_out, guests, request.args.get("promo", ""))
    except (validators.ValidationError, promo.PromoError) as e:
        return jsonify({"error": str(e)}), 400

    data = q.to_dict()
    data["free"] = availability.is_free(room.id, check_in, check_out)
    return jsonify(data)
