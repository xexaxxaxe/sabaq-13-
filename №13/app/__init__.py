from flask import Flask

import config

from . import auth, db
from .utils import dates, formatting
from .views import bookings, rooms, search


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SESSION_COOKIE_NAME"] = config.SESSION_COOKIE_NAME

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(bookings.bp)

    app.add_template_filter(formatting.money, "money")
    app.add_template_filter(formatting.nights_word, "nights")
    app.add_template_filter(formatting.guests_word, "guests")
    app.add_template_filter(dates.human_date, "date")
    app.context_processor(auth.inject_user)

    return app
