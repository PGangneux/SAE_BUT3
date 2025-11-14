from ..views import BaseModelViewSet
from ..models import Utilisateur
from ..serializers import UtilisateurSerializer


class UtilisateurViewSet(BaseModelViewSet):
    """
    Renvoie les utilisateurs
    """
    def __init__(self, **kwargs):
        super().__init__(UtilisateurSerializer, Utilisateur, **kwargs)
