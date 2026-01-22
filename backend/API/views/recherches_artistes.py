from ..views import BaseRelationShipViewSet
from ..models import Artiste, Utilisateur
from ..serializers import RecherchesArtistesSerializer
from ..permissions import IsUserOrAdmin


class RecherchesArtistesViewSet(BaseRelationShipViewSet):
    """
    Renvoie les artistes qui ont été recherché par l'utilisateur
    """

    permission_classes = [IsUserOrAdmin]

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
