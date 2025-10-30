from neomodel import db
from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import StyleMusical
from ..serializers import StyleMusicalSerializer


class StyleMusicalViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes
    """
    serializer_class = StyleMusicalSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        return StyleMusical.nodes.all()
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return StyleMusical.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.', 404)
