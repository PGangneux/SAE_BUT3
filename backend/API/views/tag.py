from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Tag
from ..serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    Renvoie les tags
    """
    serializer_class = TagSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        return Tag.nodes.all()

    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return Tag.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Tag introuvable.', 404)
