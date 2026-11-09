from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from app.services.auth_service import authenticate


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password or len(username) > 50 or len(password) > 256:
            flash("Invalid username or password.", "error")
        else:
            user = authenticate(username, password)
            if user:
                login_user(user)
                return redirect(url_for("dashboard.index"))
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
