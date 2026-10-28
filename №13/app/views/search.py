from datetime import date, timedelta

from flask import Blueprint, render_template, request

from ..services import availability, pricing
from ..utils import validators

bp = Blueprint("search", __name__)


@bp.route("/")
def index():
    tomorrow = date.today() + timedelta(days=1)
    form = {
        "check_in": request.args.get("check_in", tomorrow.isoformat()),
        "check_out": request.args.get("check_out", (tomorrow + timedelta(days=2)).isoformat()),
        "guests": request.args.get("guests", "2"),
    }

    error = None
    results = []
    try:
        check_in, check_out = validators.parse_period(form["check_in"], form["check_out"])
        guests = validators.parse_guests(form["guests"])
    except validators.ValidationError as e:
        error = str(e)
    else:
        for room in availability.free_rooms(check_in, check_out, guests):
            q = pricing.quote(room, check_in, check_out, guests)
            results.append({"room": room, "quote": q})
        results.sort(key=lambda item: item["quote"].total)

    return render_template(
        "search.html",
        form=form,
        error=error,
        results=results,
        today=date.today().isoformat(),
    )
