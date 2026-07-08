from app.extension import db
from app.models.base import BaseModel


class Maitre(BaseModel):
    __tablename__ = "maitres"

    # Clé saisie par l'utilisateur (pas d'auto-incrément)
    matricule = db.Column(db.String(50), primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))

    # Un maître peut encadrer plusieurs classes.
    # Pas de cascade delete ici : la règle métier INTERDIT la suppression
    # d'un maître qui a des classes (vérifié dans la vue avant delete).
    classes = db.relationship("Classe", back_populates="maitre")

    def __repr__(self):
        return f"<Maitre {self.matricule} {self.prenom} {self.nom}>"
