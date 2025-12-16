from ..views import BaseModelViewSet
from ..models import Nation
from ..serializers import NationSerializer


class NationViewSet(BaseModelViewSet):
    """
    Renvoie les Nations
    """

    def __init__(self, **kwargs):
        super().__init__(NationSerializer, Nation, **kwargs)
