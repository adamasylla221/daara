# Gestion d'une Daara — Projet Flask (L2 GL, ISI)

## Répartition des modules

| Membre | Module | Dépend de |
|---|---|---|
| Chef de projet | Maitre + socle transverse | — |
| Membre 2 | Classe | Maitre |
| Membre 3 | Talibe | Classe |
| Membre 4 | Progression | Talibe |

Le module **Maitre** (`app/models/maitre.py`, `app/forms/maitre.py`,
`app/views/maitre.py`, `app/templates/maitres/`) est **entièrement
implémenté** et sert de référence de style pour les 3 autres modules.

Les modules **Classe**, **Talibe**, **Progression** sont des **stubs** :
la structure (fichiers, routes, champs) est posée, les `TODO` indiquent
précisément quoi compléter (relations SQLAlchemy, règles de suppression,
`choices` des menus déroulants).

## Règles Git (obligatoires)

- Jamais de push direct sur `main`. Toujours une Pull Request + review.
- Chacun ne modifie QUE les fichiers de son module (models/forms/views/
  templates de son entité). Les fichiers transverses (`app/__init__.py`,
  `extension.py`, `config.py`, `base.html`, `exceptions/__init__.py`,
  `utils/csv_exporter.py`) ne sont modifiés que par le chef de projet,
  ou après concertation du groupe.
- Ordre de merge obligatoire : `feature/maitre` → `feature/classe` →
  `feature/talibe` → `feature/progression` (chaîne de dépendances des FK).
- Branches : `feature/maitre`, `feature/classe`, `feature/talibe`,
  `feature/progression`.

## Lancement

```bash
python -m venv venv
source venv/bin/activate   # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # puis ajuster les valeurs
flask db init
flask db migrate -m "init"
flask db upgrade
flask run
```
