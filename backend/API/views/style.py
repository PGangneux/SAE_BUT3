from ..views import BaseRelationShipViewSet
from ..models import Artiste, StyleMusical
from ..serializers import StyleRelationShipSerializer


class ArtisteStyleRelationShipViewSet(BaseRelationShipViewSet):
    def __init__(self, **kwargs):
        super().__init__(
            StyleRelationShipSerializer,
            StyleMusical,
            "artiste_uuid",
            Artiste,
            "STYLE",
            **kwargs
        )
