"""
Hiérarchie d'exceptions métier.
Règle : levées ET capturées dans la couche views. Le template
n'attrape jamais une exception directement.
"""


class DaaraException(RuntimeError):
    """Racine de toutes les exceptions métier de l'application."""
    pass


# --- Maitre --------------------------------------------------------------
class MaitreIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun maître pour le matricule : {matricule}")


class MaitreDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un maître existe déjà avec le matricule : {matricule}")


# --- Classe ----------------------------------------------------------------
class ClasseIntrouvableException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Aucune classe pour le code : {code}")


class ClasseDejaExistanteException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Une classe existe déjà avec le code : {code}")


# --- Talibe ------------------------------------------------------------------
class TalibeIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun talibé pour le matricule : {matricule}")


class TalibeDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un talibé existe déjà avec le matricule : {matricule}")


# --- Progression -------------------------------------------------------------
class ProgressionIntrouvableException(DaaraException):
    def __init__(self, progression_id):
        super().__init__(f"Aucune progression pour l'id : {progression_id}")


class ProgressionInvalideException(DaaraException):
    def __init__(self, message: str = "Progression invalide"):
        super().__init__(message)


# --- Règle transverse ---------------------------------------------------------
class SuppressionImpossibleException(DaaraException):
    """Levée quand une suppression violerait une relation existante."""
    def __init__(self, message: str):
        super().__init__(message)
