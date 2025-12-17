from ..views import BaseRelationShipViewSet
from ..models import Artiste, Utilisateur
from ..serializers import RecherchesArtistesSerializer


class RecherchesArtistesViewSet(BaseRelationShipViewSet):
    """
    Renvoie les artistes qui ont été recherché par l'utilisateur
    """

    def __init__(self, **kwargs):
        super().__init__(
            RecherchesArtistesSerializer,
            Artiste,
            "utilisateur_uuid",
            Utilisateur,
            "RECHERCHES_ARTISTES",
            "name",
            **kwargs
        )
