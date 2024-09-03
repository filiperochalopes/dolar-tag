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

    # argumentos esperados
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")
    tags = request.args.get("tags") 
    cash_in_out = request.args.get("cash_in_out")

    records = db.session.query(Record)
    # filtrando por data e tags caso esteja presente
    if date_start and date_end:  
        print("Filtrando por data...")  
        records = records.filter(Record.date.between(date_start, date_end))
    if tags:
        print("Filtrando por tags...")
        tags = [tag.strip() for tag in tags.split(",")]
        records = records.filter(Record.tags.any(Tag.name.in_(tags)))
    
    # Filtrando por entradas e saídas
    if cash_in_out == "entradas":
        records = records.filter(Record.amount > 0)
    elif cash_in_out == "saidas":
        records = records.filter(Record.amount < 0)

    records = records.order_by(Record.date.desc()).all()
    # somando todos os valores de registros
    records_sum = sum([record.amount for record in records])
    return render_template("index.html.j2", records=records, sum=records_sum)


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

    amount_type = request.form["type"]
    amount = request.form["amount"]
    if amount_type == "saida":
        amount = -float(amount)
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
        amount_type = request.form["type"]
        amount = request.form["amount"]
        if amount_type == "saida":
            amount = -float(amount)
        record.amount = amount
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
