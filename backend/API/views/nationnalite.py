from neomodel import db
from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Nationnalite
from ..serializers import NationnaliteSerializer


class NationnaliteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes
    """
    serializer_class = NationnaliteSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Nationnalite.nodes.all()
    
    def get_object(self):
        try:
            return Nationnalite.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.', 404)
