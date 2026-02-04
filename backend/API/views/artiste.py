from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Artiste
from ..serializers import ArtisteSerializer


class ArtisteViewSet(BaseModelViewSet):
    """
    Renvoie les artistes
    """

    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, "name", **kwargs)
