from ..views import BaseModelViewSet
from ..models import Tag
from ..serializers import TagSerializer


class TagViewSet(BaseModelViewSet):
    """
    Renvoie les tags
    """

    def __init__(self, **kwargs):
        super().__init__(TagSerializer, Tag, **kwargs)
