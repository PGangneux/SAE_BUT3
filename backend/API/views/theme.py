from ..views import BaseModelViewSet
from ..models import Theme
from ..serializers import ThemeSerializer


class ThemeViewSet(BaseModelViewSet):
    """
    Renvoie les thèmes
    """

    def __init__(self, **kwargs):
        super().__init__(ThemeSerializer, Theme, **kwargs)
