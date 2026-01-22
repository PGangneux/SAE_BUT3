from ..views import BaseModelViewSet
from ..models import Utilisateur
from ..serializers import UtilisateurSerializer
from ..permissions import IsUserOrAdmin
from rest_framework.permissions import AllowAny


class UtilisateurViewSet(BaseModelViewSet):
    """
    Renvoie les utilisateurs
    """

    # permission_classes = [IsUserOrAdmin]

    def get_permissions(self):
        if self.action in ["retrieve", "update", "destroy"]:
            return [IsUserOrAdmin()]
        return [AllowAny()]

    def __init__(self, **kwargs):
        super().__init__(UtilisateurSerializer, Utilisateur, **kwargs)
