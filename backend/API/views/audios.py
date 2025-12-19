from ..views import BaseRelationShipViewSet
from ..models import Audio, Extrait
from ..serializers import AudiosSerializer


class AudiosViewSet(BaseRelationShipViewSet):
    """
    Renvoie les audio qui sont connecté à l'extrait
    """

    def __init__(self, **kwargs):
        super().__init__(
            AudiosSerializer,
            Audio,
            "extrait_uuid",
            Extrait,
            "AUDIOS",
            "name",
            **kwargs
        )