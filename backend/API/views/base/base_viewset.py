from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from neomodel import StructuredNode
from ..base import BaseGenericViewSet

class BaseModelViewSet(BaseGenericViewSet, ModelViewSet):
    """
    Classe de base pour les ModelViewSets classiques
    """
    def __init__(self, serializer_class: Serializer, model_class: StructuredNode, search_field: str = None, **kwargs):
        super().__init__(serializer_class, model_class, search_field, **kwargs)