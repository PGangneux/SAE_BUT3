from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Utilisateur
from ..serializers import UtilisateurSerializer


class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    Renvoie les utilisateurs
    """
    serializer_class = UtilisateurSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        return Utilisateur.nodes.all()
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return Utilisateur.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Utilisateur introuvable.', 404)