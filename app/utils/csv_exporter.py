import csv
import io

from flask import make_response


def exporter_csv(nom_fichier: str, entetes: list, lignes: list):
    """
    Génère une réponse HTTP de type fichier CSV téléchargeable.
    Appelé UNIQUEMENT depuis la couche views.

    :param nom_fichier: nom du fichier proposé au téléchargement (ex: 'talibes.csv')
    :param entetes: liste des noms de colonnes (ligne d'en-tête)
    :param lignes: liste de listes/tuples, une par enregistrement
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(entetes)
    for ligne in lignes:
        writer.writerow(ligne)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={nom_fichier}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response
