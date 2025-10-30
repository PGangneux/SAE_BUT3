from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Theme
from ..serializers import ThemeSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    """
    Renvoie les thèmes
    """
    serializer_class = ThemeSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        return Theme.nodes.all()

    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return Theme.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Thème introuvable.', 404)
