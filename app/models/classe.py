from app.extension import db
from app.models.base import BaseModel


class Classe(BaseModel):
    __tablename__ = "classes"
    # Clé saisie par l'utilisateur
    code = db.Column(db.String(50), primary_key=True)
    libelle = db.Column(db.String(150), nullable=False)
    niveau = db.Column(db.String(50))

    # FK obligatoire vers Maitre
    maitre_matricule = db.Column(
        db.String(50), db.ForeignKey("maitres.matricule"), nullable=False
    )
    maitre = db.relationship("Maitre", back_populates="classes")

    # Une classe regroupe plusieurs talibés.
    # Pas de cascade delete : la règle métier INTERDIT la suppression
    # d'une classe qui a des talibés (vérifié dans la vue avant delete).
    talibes = db.relationship("Talibe", back_populates="classe")

    def __repr__(self):
        return f"<Classe {self.code} {self.libelle}>"
