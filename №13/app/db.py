import os
import sqlite3

from flask import g

import config

from . import seed

SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def get_db():
    if "db" not in g:
        if not os.path.exists(config.DATABASE):
            init_db()
        g.db = sqlite3.connect(config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(config.DATABASE)
    with open(SCHEMA_FILE, encoding="utf-8") as f:
        db.executescript(f.read())
    seed.fill(db)
    db.commit()
    db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    init_db()
