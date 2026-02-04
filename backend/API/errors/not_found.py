from rest_framework.exceptions import NotFound as nf
from neomodel import StructuredNode


class NotFound(nf):
    """
    L'instance de Node n'a pas été trouvé avec l'uuid fourni
    """

    def __init__(self, Class: StructuredNode = None):
        super().__init__({"Not Found": Class.__name__ if Class is not None else None})
