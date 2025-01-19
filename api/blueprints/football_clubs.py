from collections import OrderedDict
from typing import Union, Iterable
from flask import Blueprint, render_template, redirect, flash, url_for, abort, request
# from html import escape, unescape

__all__ = [
    "serverless",
    "blueprint"
]

# Self data store in runtime and flash messages
serverless = False
blueprint = Blueprint(
    "football_club",
    __name__,
    template_folder="../../templates/_3",
    url_prefix="/assignments/_3/football-clubs"
)

class StringData(OrderedDict):
    def __init__(self) -> None:
        self.last_id = 0
        super().__init__()

    def clear(self) -> None:
        self.last_id = 0
        return super().clear()

    def add(self, name: Union[str, Iterable[str]]) -> None:
        if isinstance(name, str):
            self.last_id += 1
            self[self.last_id] = name
        else:
            for n in name:
                self.last_id += 1
                self[self.last_id] = n

clubs = StringData()
players = StringData()

rot13 = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
)

def _clubs_init():
    global clubs
    clubs.clear()
    clubs.add(map(lambda s: s.translate(rot13), ['Yvirecbby', 'Nefrany', 'Abggvatunz Sberfg', 'Arjpnfgyr Havgrq', 'Nfgba Ivyyn', 'Puryfrn', 'Znapurfgre Pvgl', 'Obhearzbhgu', 'Oeragsbeq', 'Oevtugba & Ubir Nyovba']))

def _players_init():
    global players
    players.clear()
    players.add(map(lambda s: s.translate(rot13), ['Zbunzrq Fnynu', 'Reyvat Unnynaq', 'Nyrknaqre Vfnx', 'Pbyr Cnyzre', 'Oelna Zorhzb', 'Puevf Jbbq', 'Lbnar Jvffn', 'Zngurhf Phaun', 'Avpbynf Wnpxfba', 'Byyvr Jngxvaf']))

_clubs_init()
_players_init()

pages = {
    "club": (
        clubs,
        _clubs_init
    ),
    "player": (
        players,
        _players_init
    )
}

@blueprint.route("/")
def index():
    return render_template("index.html", title="Home", target="home", count_clubs=len(clubs), count_players=len(players))

@blueprint.route("/<string:target>")
def page(target: str):
    if target not in pages:
        return abort(404)
    return render_template("view-edit-page/index.html", title=(target.capitalize() + "s"), target=target, items=pages[target][0].items())

@blueprint.route("/<string:target>/reset")
def page_reset(target: str):
    if target not in pages:
        return abort(404)
    pages[target][1]()
    return redirect(url_for("football_club.page", target=target))

@blueprint.route("/<string:target>/add", methods=["GET", "POST"])
def page_add(target: str):
    if target not in pages:
        return abort(404)

    if request.method == "POST":
        name = request.form["name"]
        if name is not None and name.strip() != "":
            print(name)
            pages[target][0].add(name)
            return redirect(url_for("football_club.page", target=target))
        else:
            flash("Name cannot be empty.", "error")

    return render_template("view-edit-page/add.html", title=f"Add {target.capitalize()}", target=target)

@blueprint.route("/<string:target>/delete")
def page_delete(target: str):
    if target not in pages:
        return abort(404)

    id = request.args.get("id")
    if id is not None and id.isdecimal() and (id := int(id)) in pages[target][0]:
        del pages[target][0][id]

    return redirect(url_for("football_club.page", target=target))

@blueprint.route("/<string:target>/update", methods=["GET", "POST"])
def page_update(target: str):
    id = None
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        if id is not None and id.isdecimal() and name is not None and name.strip() != "":
            if (id := int(id)) in pages[target][0]:
                pages[target][0][id] = name
                return redirect(url_for("football_club.page", target=target))
        flash("Name cannot be empty.", "error")

    id = request.args.get("id") if id is None else id
    if id is None or (isinstance(id, str) and not id.isdecimal()) or (id := int(id)) not in pages[target][0]:
        return redirect(url_for("football_club.page", target=target))

    return render_template("view-edit-page/update.html", title=(target.capitalize() + "s"), target=target, item=(id, pages[target][0][id]))
