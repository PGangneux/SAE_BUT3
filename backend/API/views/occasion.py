from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Interview, Occasion
from ..serializers import OccasionSerializer


class OccasionViewSet(BaseModelViewSet):
    """
    Renvoie les interviews
    """

    def __init__(self, **kwargs):
        super().__init__(OccasionSerializer, Occasion, "name", **kwargs)
