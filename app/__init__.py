import os

from flask import Flask, render_template, flash, redirect, url_for

from config import config_by_name
from app.extension import db, migrate, csrf
from app.exceptions import DaaraException


def create_app(config_name=None):
    """App factory. Ne pas mettre de logique métier ici."""
    app = Flask(__name__)

    config_name = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[config_name])

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Import des modèles pour que Flask-Migrate les détecte
    from app.models import maitre, classe, talibe, progression  # noqa: F401

    # Enregistrement des Blueprints
    from app.views.main import bp_main
    from app.views.maitre import bp_maitres
    from app.views.classe import bp_classes
    from app.views.talibe import bp_talibes
    from app.views.progression import bp_progressions

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_maitres)
    app.register_blueprint(bp_classes)
    app.register_blueprint(bp_talibes)
    app.register_blueprint(bp_progressions)

    # Gestion centralisée des exceptions métier :
    # chaque vue peut aussi faire son propre try/except si elle a besoin
    # d'un comportement particulier, mais ce handler sert de filet de
    # sécurité pour ne jamais afficher une page d'erreur brute à l'utilisateur.
    @app.errorhandler(DaaraException)
    def gerer_exception_metier(erreur):
        flash(str(erreur), "danger")
        return redirect(url_for("main.accueil"))

    return app
