from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Artiste
from ..serializers import ArtisteSerializer


class ArtisteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes
    """
    serializer_class = ArtisteSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Artiste.nodes.all()
    
    def get_object(self):
        try:
            return Artiste.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.', 404)
