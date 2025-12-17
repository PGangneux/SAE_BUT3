from rest_framework.exceptions import ValidationError


class ValidatorUnique(ValidationError):
    """
    Erreur de validation du champ
    Une valeur déjà existante a été renseigné
    """

    def __init__(self, detail: str = ""):
        super().__init__({"Unique Property": detail})
