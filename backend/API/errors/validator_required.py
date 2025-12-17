from rest_framework.exceptions import ValidationError

class ValidatorRequired(ValidationError):
    """
    Erreur, code status et message pour champ unique
    """
    def __init__(self, detail:str=''):
        super().__init__({'Required Property': detail})