from ..views import BaseModelViewSet
from ..models import StyleMusical
from ..serializers import StyleMusicalSerializer


class StyleMusicalViewSet(BaseModelViewSet):
    """
    Renvoie les artistes
    """

    def __init__(self, **kwargs):
        super().__init__(StyleMusicalSerializer, StyleMusical, **kwargs)
