from datetime import datetime, timezone

from app.extension import db


def _maintenant():
    """Horodatage UTC timezone-aware (remplace l'obsolète datetime.utcnow())."""
    return datetime.now(timezone.utc)


class BaseModel(db.Model):
    """
    Classe abstraite dont héritent toutes les entités.
    __abstract__ = True => aucune table créée pour BaseModel elle-même.
    """
    __abstract__ = True

    cree_le = db.Column(db.DateTime(timezone=True), default=_maintenant, nullable=False)
    maj_le = db.Column(
        db.DateTime(timezone=True),
        default=_maintenant,
        onupdate=_maintenant,
        nullable=False,
    )