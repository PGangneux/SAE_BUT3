from ..views import BaseRelationShipViewSet
from ..models import Interview, Utilisateur
from ..serializers import RegarderInterviewsSerializer
from ..permissions import IsUserOrAdmin


class RegarderInterviewsViewSet(BaseRelationShipViewSet):
    """
    Renvoie les interviews qui ont été regardé par l'utilisateur
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        super().__init__(
            RegarderInterviewsSerializer,
            Interview,
            "utilisateur_uuid",
            Utilisateur,
            "REGARDER_INTERVIEWS",
            "title",
            **kwargs
        )
