"""
Point d'entrée de l'application.
Ne pas mettre de logique métier ici : uniquement la création de l'app.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
