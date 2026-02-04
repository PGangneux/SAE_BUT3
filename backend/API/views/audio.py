from ..views import BaseModelViewSet
from ..models import Audio
from ..serializers import AudioSerializer


class AudioViewSet(BaseModelViewSet):
    """
    Renvoie les audios
    """

    def __init__(self, **kwargs):
        super().__init__(AudioSerializer, Audio, "name", **kwargs)