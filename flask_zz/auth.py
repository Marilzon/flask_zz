import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_zz.database import open_database

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

blueprint.route("/sign-in", methods=("GET", "POST"))
def sign_in():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        database = open_database()
        error = None

        if not username:
            error = "Username is required."
        if not password:
            error = "Password is required."

        if error is None:
            try:
                database.execute(
                    "INSERT INTO user (username, password) VALUES (?. ?)",
                    (username, generate_password_hash(password))
                )
                database.commit()
            except database.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/sign-in.html")
