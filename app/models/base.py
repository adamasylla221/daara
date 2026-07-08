from datetime import datetime

from app.extension import db


class BaseModel(db.Model):
    """
    Classe abstraite dont héritent toutes les entités.
    __abstract__ = True => aucune table créée pour BaseModel elle-même.
    """
    __abstract__ = True

    cree_le = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    maj_le = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
