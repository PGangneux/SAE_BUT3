from ..views import BaseRelationShipViewSet
from ..models import Extrait, Utilisateur
from ..serializers import RegarderExtraitsSerializer


class RegarderExtraitsViewSet(BaseRelationShipViewSet):
    """
    Renvoie les extraits qui ont été regardé par l'utilisateur
    """
    def __init__(self, **kwargs):
        super().__init__(RegarderExtraitsSerializer, Extrait, 'utilisateur_uuid', Utilisateur, 'REGARDER_EXTRAITS', 'title', **kwargs)
