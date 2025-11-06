from rest_framework.exceptions import ValidationError
from neomodel import StructuredNode

class ContextError(ValidationError):
    """
    Erreur, code status et message pour erreur de contexte
    """
    def __init__(self, Class:StructuredNode=None):
        super().__init__({'Context error': Class.__name__ if Class is not None else None}, 400)