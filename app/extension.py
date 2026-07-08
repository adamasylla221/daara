"""
Instances partagées des extensions Flask.
Ce fichier ne fait AUCUNE logique : il ne fait qu'instancier.
On importe ces objets partout ailleurs (models, __init__.py, etc.)
pour éviter les imports circulaires.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
