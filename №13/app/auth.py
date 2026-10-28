import sqlite3
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint("auth", __name__)


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    user = get_db().execute(
        "SELECT * FROM users WHERE id = ? AND username = ?",
        (user_id, session.get("username")),
    ).fetchone()
    if user is None:
        session.pop("user_id", None)
        session.pop("username", None)
    return user


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if current_user() is None:
            flash("Сначала войдите в аккаунт")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapper


def inject_user():
    return {"user": current_user()}


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        password2 = request.form["password2"]

        if not username or not password:
            flash("Заполните все поля")
        elif len(password) < 4:
            flash("Пароль должен быть не короче 4 символов")
        elif password != password2:
            flash("Пароли не совпадают")
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password, method="pbkdf2:sha256")),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("Такой пользователь уже существует")
            else:
                flash("Регистрация прошла успешно! Теперь войдите.")
                return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            flash("Неверный логин или пароль")
        else:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Добро пожаловать, {user['username']}!")
            return redirect(url_for("search.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из аккаунта")
    return redirect(url_for("search.index"))
