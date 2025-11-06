from rest_framework.exceptions import NotFound as nf
from neomodel import StructuredNode

class NotFound(nf):
    """
    Erreur, code et message pour instance non trouvé
    """
    def __init__(self, Class:StructuredNode=None):
        super().__init__({'Not Found': Class.__name__ if Class is not None else None})