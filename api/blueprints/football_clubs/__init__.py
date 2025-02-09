from functools import cache
from flask import Blueprint, render_template, redirect, flash, url_for, abort, request
from sqlalchemy import exc as sqlalchemy_exceptions
from api.db import football_clubs_db as db
from api.blueprints.football_clubs.db_schema import Nationality, PlayerPosition, Player, Club

__all__ = [
    "serverless",
    "blueprint"
]

@cache
def get_nationalities():
    return db.session.query(Nationality.id, Nationality.name).all()

@cache
def get_positions():
    return db.session.query(PlayerPosition.id, PlayerPosition.name).all()

serverless = False
blueprint = Blueprint(
    "football_club",
    __name__,
    template_folder="../../../templates/3",
    url_prefix="/assignments/3/football-clubs"
)

def is_decimal(value: str | None) -> int | None:
    return int(value) if value is not None and value.isdecimal() else None

@blueprint.route("/")
def home():
    club_count = db.session.query(Club).count()
    player_count = db.session.query(Player).count()

    return render_template("home.index.html", title="Home", target="home", count_clubs=club_count, count_players=player_count)

@blueprint.route("/<string:target>")
def page(target: str):
    query = request.args.get("query")
    if target == "club":
        if query is not None: items = db.session.query(Club.id, Club.name).filter(Club.name.ilike(f"%{query}%")).all()
        else: items = db.session.query(Club.id, Club.name).all()
    elif target == "player":
        if query is not None: items = db.session.query(Player.id, Player.name).filter(Player.name.ilike(f"%{query}%")).all()
        else: items = db.session.query(Player.id, Player.name).all()
    else:
        return abort(404)

    return render_template("list.index.html", title=(target.capitalize() + "s"), target=target, items=items, query=query if query else "")

@blueprint.route("/<string:target>/<int:id>")
def page_info(target: str, id: int):
    image_url: str
    data: list[tuple[str, str]]

    if target == "club":
        club = db.session.query(Club.name, Club.image_url).filter(Club.id == id).one_or_none()
        if club is None: return abort(404)
        image_url = club[1]
        data = [
            ("Name", club[0]),
            ("Number of Players", str(db.session.query(Player).filter(Player.club_id == id).count()))
        ]
    elif target == "player":
        player = db.session.query(Player).filter(Player.id == id).one_or_none()
        if player is None: return abort(404)
        image_url = player.image_url
        data = [
            ("Name", player.name),
            ("Club", player.club.name),
            ("Position", player.position.name),
            ("Nationality", player.nationality.name)
        ]

    return render_template("info.html", title=target.capitalize(), target=target, img_url=image_url, obj=data, id=id)

@blueprint.route("/<string:target>/add", methods=["GET", "POST"], endpoint="page_add")
@blueprint.route("/<string:target>/update", methods=["GET", "POST"], endpoint="page_update")
def page_add_update(target: str):
    if target == "club":
        if request.method == "POST":
            try:
                name = request.form["name"]
                image_url = request.form["image_url"]
                assert len(name) < 256 and len(image_url) < 2048
            except:
                return abort(400)

            if request.endpoint == "football_club.page_update":
                if (id := is_decimal(request.form.get("id"))) == None: return abort(400)

                db.session.query(Club).filter(Club.id == id).update({"name": name, "image_url": image_url})
                db.session.commit()
                return redirect(url_for("football_club.page", target=target))
            else:
                try:
                    db.session.add(Club(name=name, image_url=image_url))
                    db.session.commit()
                    return redirect(url_for("football_club.page", target=target))
                except sqlalchemy_exceptions.IntegrityError:
                    flash("Club name is duplicate.", "error")

        fields = [
            ("name", "Name", None),
            ("image_url", "Image URL", None)
        ]
    elif target == "player":
        if request.method == "POST":
            try:
                data = [(x, int(request.form[x]) if x.endswith("_id") else request.form[x]) for x in ("name", "club_id", "position_id", "nationality_id", "image_url")]
                assert len(data[0][1]) < 256 and len(data[4][1]) < 2048 # type: ignore
            except:
                return abort(400)

            if request.endpoint == "football_club.page_update":
                if (id := is_decimal(request.form.get("id"))) == None: return abort(400)

                db.session.query(Player).filter(Player.id == id).update(dict(data))
            else:
                db.session.add(Player(**dict(data)))

            db.session.commit()

            return redirect(url_for("football_club.page", target=target))

        if not (clubs := db.session.query(Club.id, Club.name).all()):
            flash("No clubs available, Please add a club before adding players", "error")
            fields = []
        else:
            fields = [
                ("name", "Name", None),
                ("club_id", "Club", clubs),
                ("position_id", "Position", get_positions()),
                ("nationality_id", "Nationality", get_nationalities()),
                ("image_url", "Image URL", None)
            ]
    else:
        return abort(404)

    if request.endpoint == "football_club.page_update":
        fields.insert(0, ("id", "ID", None))
        obj = None

        if (id := is_decimal(request.args.get("id"))) == None: return abort(400)
        if target == "club": obj = db.session.query(Club).filter(Club.id == id).one_or_none()
        elif target == "player": obj = db.session.query(Player).filter(Player.id == id).one_or_none()

        if obj is None: return abort(404)

        fields = [field + (getattr(obj, field[0], ""), ) for field in fields]
    else:
        fields = [(field[0], field[1], field[2], "") for field in fields]

    endpoint = request.endpoint
    if endpoint == None: return abort(404)

    return render_template("update.html", edit=endpoint.split("_")[-1].capitalize(), target=target, fields=fields)

@blueprint.route("/<string:target>/delete")
def page_delete(target: str):
    if (id := is_decimal(request.args.get("id"))) == None: return abort(400)

    obj = None
    if target == "club": obj = db.session.query(Club).filter(Club.id == id).one_or_none()
    elif target == "player": obj = db.session.query(Player).filter(Player.id == id).one_or_none()
    else: return abort(404)

    if obj:
        db.session.delete(obj)
        db.session.commit()

    return redirect(url_for("football_club.page", target=target))
