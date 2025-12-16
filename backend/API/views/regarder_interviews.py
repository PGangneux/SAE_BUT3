from ..views import BaseRelationShipViewSet
from ..models import Interview, Utilisateur
from ..serializers import RegarderInterviewsSerializer


class RegarderInterviewsViewSet(BaseRelationShipViewSet):
    """
    Renvoie les interviews qui ont été regardé par l'utilisateur
    """

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
