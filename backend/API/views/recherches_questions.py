from ..views import BaseRelationShipViewSet
from ..models import Question, Utilisateur
from ..serializers import RecherchesQuestionsSerializer
from ..permissions import IsUserOrAdmin


class RecherchesQuestionsViewSet(BaseRelationShipViewSet):
    """
    Renvoie les questions qui ont été recherché par l'utilisateur
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        super().__init__(
            RecherchesQuestionsSerializer,
            Question,
            "utilisateur_uuid",
            Utilisateur,
            "RECHERCHES_QUESTIONS",
            "texte",
            **kwargs
        )
