from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Artiste, StyleMusical
from ..serializers import ArtisteSerializer


class ArtisteViewSet(BaseModelViewSet):
    """
    Renvoie les artistes
    """

    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, "name", **kwargs)


class StyleMusicalArtisteViewSet(SubBaseModelViewSet):
    """
    Renvoie les artistes en fonction d'un style musical
    """

    def __init__(self, **kwargs):
        super().__init__(
            ArtisteSerializer,
            Artiste,
            "stylemusical_uuid",
            StyleMusical,
            "STYLE",
            "name",
            **kwargs
        )
