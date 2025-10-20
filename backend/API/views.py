# views.py
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from neomodel.exceptions import DoesNotExist, UniqueProperty
from .models import Theme
from .serializers import ThemeSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    """
    ViewSet simple pour le modèle Theme (Neo4j via neomodel).
    Fournit les opérations CRUD de base.
    """
    serializer_class = ThemeSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Theme.nodes.all()

    def get_object(self):
        try:
            return Theme.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Thème introuvable.')
