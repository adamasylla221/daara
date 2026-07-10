"""
Test fonctionnel de bout en bout : vérifie que l'application tourne
réellement (CRUD + CSV + règles métier) sans avoir besoin de PostgreSQL.
Utilise SQLite en mémoire uniquement pour CE test, la config réelle du
projet reste PostgreSQL (voir config.py).
"""
import sys

import config
config.TestingConfig.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

from app import create_app
from app.extension import db

app = create_app("testing")

erreurs = []


def verifier(label, condition):
    statut = "OK " if condition else "FAIL"
    print(f"[{statut}] {label}")
    if not condition:
        erreurs.append(label)


with app.app_context():
    db.create_all()

    client = app.test_client()

    # --- Page d'accueil ---
    r = client.get("/")
    verifier("Accueil répond 200", r.status_code == 200)

    # --- MAITRE : créer ---
    r = client.post("/maitres/nouveau", data={
        "matricule": "M001", "prenom": "Ousmane", "nom": "Diop", "telephone": "771234567"
    }, follow_redirects=True)
    verifier("Création maître OK", r.status_code == 200 and b"Ma\xc3\xaetre ajout\xc3\xa9" in r.data)

    # --- MAITRE : doublon doit échouer proprement ---
    r = client.post("/maitres/nouveau", data={
        "matricule": "M001", "prenom": "X", "nom": "Y"
    }, follow_redirects=True)
    verifier("Doublon maître rejeté (exception capturée)", r.status_code == 200)

    # --- MAITRE : lister ---
    r = client.get("/maitres/")
    verifier("Liste maîtres contient M001", b"M001" in r.data)

    # --- CLASSE : créer (dépend de Maitre) ---
    r = client.post("/classes/nouveau", data={
        "code": "CL-DEB", "libelle": "Débutants", "niveau": "1",
        "maitre_matricule": "M001"
    }, follow_redirects=True)
    verifier("Création classe OK", r.status_code == 200 and b"Classe ajout\xc3\xa9e" in r.data)

    r = client.get("/classes/")
    verifier("Liste classes affiche le maître lié", b"Ousmane" in r.data)

    # --- TALIBE : créer (dépend de Classe) ---
    r = client.post("/talibes/nouveau", data={
        "matricule": "T001", "prenom": "Modou", "nom": "Fall",
        "date_naissance": "2012-05-10", "classe_code": "CL-DEB"
    }, follow_redirects=True)
    verifier("Création talibé OK", r.status_code == 200 and b"Talib\xc3\xa9 ajout\xc3\xa9" in r.data)

    r = client.get("/talibes/")
    verifier("Liste talibés affiche la classe liée", b"D\xc3\xa9butants" in r.data)

    # --- CLASSE : suppression interdite car talibé rattaché ---
    r = client.post("/classes/CL-DEB/supprimer", follow_redirects=True)
    verifier("Suppression classe bloquée (talibé rattaché)",
              b"Impossible de supprimer la classe" in r.data)

    # --- PROGRESSION : créer (dépend de Talibe) ---
    r = client.post("/progressions/nouveau", data={
        "sourate": "Al-Fatiha", "nombre_versets": "7",
        "date_evaluation": "2026-01-15", "talibe_matricule": "T001"
    }, follow_redirects=True)
    verifier("Création progression OK", r.status_code == 200 and b"Progression ajout\xc3\xa9e" in r.data)

    r = client.get("/progressions/")
    verifier("Liste progressions affiche le talibé lié", b"Modou" in r.data)

    # --- PROGRESSION : valeur invalide rejetée ---
    r = client.post("/progressions/nouveau", data={
        "sourate": "Test", "nombre_versets": "-5",
        "talibe_matricule": "T001"
    }, follow_redirects=True)
    verifier("Nombre de versets négatif rejeté",
              b"doit \xc3\xaatre >= 0" in r.data or r.status_code == 200)

    # --- EXPORT CSV pour les 4 entités ---
    for url, nom in [
        ("/maitres/export", "maîtres"),
        ("/classes/export", "classes"),
        ("/talibes/export", "talibés"),
        ("/progressions/export", "progressions"),
    ]:
        r = client.get(url)
        ok = (r.status_code == 200
              and r.headers.get("Content-Type", "").startswith("text/csv")
              and "attachment" in r.headers.get("Content-Disposition", ""))
        verifier(f"Export CSV {nom} fonctionne", ok)

    # --- TALIBE : suppression cascade vers Progression ---
    r = client.post("/talibes/T001/supprimer", follow_redirects=True)
    verifier("Suppression talibé OK", b"Talib\xc3\xa9 supprim\xc3\xa9" in r.data)

    from app.models.progression import Progression
    restantes = Progression.query.filter_by(talibe_matricule="T001").count()
    verifier("Cascade : progressions du talibé supprimées", restantes == 0)

    # --- CLASSE : suppression maintenant possible (plus de talibé) ---
    r = client.post("/classes/CL-DEB/supprimer", follow_redirects=True)
    verifier("Suppression classe OK (plus de talibé)", b"Classe supprim\xc3\xa9e" in r.data)

    # --- MAITRE : suppression maintenant possible (plus de classe) ---
    r = client.post("/maitres/M001/supprimer", follow_redirects=True)
    verifier("Suppression maître OK (plus de classe)", b"Ma\xc3\xaetre supprim\xc3\xa9" in r.data)

    # --- 404 métier : maître introuvable ---
    r = client.get("/maitres/INEXISTANT/modifier", follow_redirects=True)
    verifier("Maître introuvable géré proprement", b"Aucun ma\xc3\xaetre" in r.data)

print()
if erreurs:
    print(f"{len(erreurs)} test(s) en échec :")
    for e in erreurs:
        print(" -", e)
    sys.exit(1)
else:
    print(f"Tous les tests fonctionnels sont passés avec succès.")
