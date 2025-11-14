from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Artiste, Nation, StyleMusical
from ..serializers import ArtisteSerializer


class ArtisteViewSet(BaseModelViewSet):
    """
    Renvoie les artistes
    """
    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, 'name', **kwargs)


class StyleMusicalArtisteViewSet(SubBaseModelViewSet):
    """
    Renvoie les artistes en fonction d'un style musical
    """
    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, 'stylemusical_uuid', StyleMusical, 'STYLE', 'name', **kwargs)


class NationArtisteViewSet(SubBaseModelViewSet):
    """
    Renvoie les artistes en fonction de leur nationnalite
    """
    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, 'nation_uuid', Nation, 'NATIONALITE', 'name', **kwargs)
