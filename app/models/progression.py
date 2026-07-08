from app.extension import db
from app.models.base import BaseModel #classe de base pour contenir des attributs communs (ex: created_at, updated_at...)


class Progression(BaseModel):
    __tablename__ = "progressions"

    # Clé auto-générée (seule entité dans ce cas)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sourate = db.Column(db.String(150), nullable=False)
    nombre_versets = db.Column(db.Integer, nullable=False)
    date_evaluation = db.Column(db.Date)
    observations = db.Column(db.Text)

    # FK obligatoire vers Talibe
    talibe_matricule = db.Column(
        db.String(50), db.ForeignKey("talibes.matricule"), nullable=False
    )
    talibe = db.relationship("Talibe", back_populates="progressions")

    def __repr__(self):
        return f"<Progression {self.id} {self.sourate}>"
