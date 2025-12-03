from rest_framework.exceptions import ValidationError

class OrderError(ValidationError):
    """
    Erreur, code status et message pour champs d'order inexistant
    """
    def __init__(self, order: str):
        super().__init__({'Order error': order})