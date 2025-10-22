from neomodel import db
from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Nation
from ..serializers import NationSerializer


class NationViewSet(viewsets.ModelViewSet):
    """
    Renvoie les Nations
    """
    serializer_class = NationSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Nation.nodes.all()
    
    def get_object(self):
        try:
            return Nation.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Nation introuvable.', 404)
