from ..views import BaseRelationShipViewSet
from ..models import Extrait, Utilisateur
from ..serializers import RegarderExtraitsSerializer
from ..permissions import IsUserOrAdmin


class RegarderExtraitsViewSet(BaseRelationShipViewSet):
    """
    Renvoie les extraits qui ont été regardé par l'utilisateur
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        super().__init__(
            RegarderExtraitsSerializer,
            Extrait,
            "utilisateur_uuid",
            Utilisateur,
            "REGARDER_EXTRAITS",
            "title",
            **kwargs
        )
