"""Full-stack bookmarks app: register/login, per-user bookmark CRUD."""

import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import models

DB_PATH = os.path.join(os.path.dirname(__file__), "bookmarks.db")


def create_app(db_path=DB_PATH, secret_key="dev-secret-change-me"):
    app = Flask(__name__)
    app.secret_key = secret_key
    connection = models.get_connection(db_path)

    def current_user():
        user_id = session.get("user_id")
        return models.get_user_by_id(connection, user_id) if user_id else None

    def login_required(view):
        def wrapped(*args, **kwargs):
            if not current_user():
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        wrapped.__name__ = view.__name__
        return wrapped

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                flash("Username and password are required.")
                return render_template("register.html")

            if models.get_user_by_username(connection, username):
                flash("That username is already taken.")
                return render_template("register.html")

            user_id = models.create_user(connection, username, generate_password_hash(password))
            session["user_id"] = user_id
            return redirect(url_for("index"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            user = models.get_user_by_username(connection, username)
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                return redirect(url_for("index"))

            flash("Invalid username or password.")
            return render_template("login.html")

        return render_template("login.html")

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/", methods=["GET", "POST"])
    @login_required
    def index():
        user = current_user()

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            url = request.form.get("url", "").strip()
            if title and url:
                models.add_bookmark(connection, user["id"], title, url)
            return redirect(url_for("index"))

        bookmarks = models.list_bookmarks(connection, user["id"])
        return render_template("bookmarks.html", bookmarks=bookmarks, username=user["username"])

    @app.post("/delete/<int:bookmark_id>")
    @login_required
    def delete(bookmark_id):
        user = current_user()
        models.delete_bookmark(connection, user["id"], bookmark_id)
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
