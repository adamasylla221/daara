from flask import Blueprint, render_template

from app.models.maitre import Maitre
from app.models.classe import Classe
from app.models.talibe import Talibe
from app.models.progression import Progression

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def accueil() -> str:
    nb_maitres = Maitre.query.count()
    nb_classes = Classe.query.count()
    nb_talibes = Talibe.query.count()

    dernieres_progressions = (
        Progression.query
        .order_by(Progression.date_evaluation.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "main/index.html",
        nb_maitres=nb_maitres,
        nb_classes=nb_classes,
        nb_talibes=nb_talibes,
        progressions=dernieres_progressions,
    )