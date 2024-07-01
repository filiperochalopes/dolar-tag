import datetime

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
from werkzeug.security import check_password_hash

from . import db
from .models import Record, Tag, User

routes = Blueprint("routes", __name__)


@routes.before_app_request
def before_request():
    g.user = None
    if "user_id" in session:
        g.user = User.query.get(session["user_id"])


@routes.route("/")
def index():
    if not g.user:
        return redirect(url_for("routes.login"))

    records = Record.query.filter_by(user_id=g.user.id).all()
    return render_template("index.html.j2", records=records)


@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("routes.index"))
        else:
            flash("Login Failed. Check your username and/or password.")

    return render_template("login.html.j2")


@routes.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("routes.login"))


@routes.route("/add-record", methods=["POST"])
def add_record():
    if not g.user:
        return redirect(url_for("routes.login"))

    amount = request.form["amount"]
    description = request.form["description"]
    date = datetime.date.fromisoformat(request.form["date"])
    tags = request.form["tags"].split(",")

    new_record = Record(
        amount=amount, description=description, date=date, user_id=g.user.id
    )
    db.session.add(new_record)
    db.session.commit()

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name.strip()).first()
        if not tag:
            tag = Tag(name=tag_name.strip())
        new_record.tags.append(tag)

    db.session.commit()

    return redirect(url_for("routes.index"))


@routes.route("/edit-record/<int:id>", methods=["GET", "POST"])
def edit_record(id):
    if not g.user:
        return redirect(url_for("routes.login"))

    record = Record.query.get_or_404(id)

    if request.method == "POST":
        record.amount = request.form["amount"]
        record.description = request.form["description"]
        record.date = datetime.date.fromisoformat(request.form["date"])
        db.session.commit()

        record.tags.clear()
        tags = request.form["tags"].split(",")

        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
            record.tags.append(tag)

        db.session.commit()
        return redirect(url_for("routes.index"))

    tags = ", ".join([tag.name for tag in record.tags])
    return render_template("edit_record.html.j2", record=record, tags=tags)
