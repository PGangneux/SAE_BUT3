from rest_framework.exceptions import ValidationError
from neomodel import StructuredNode


class ContextError(ValidationError):
    """
    Erreur dans le context
    Node de context manquant
    La vue demande un node dans le context mais n'en ressoit pas
    """

    def __init__(self, Class: StructuredNode = None):
        super().__init__(
            {"Context error": Class.__name__ if Class is not None else None}
        )
