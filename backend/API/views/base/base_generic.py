from django.http import HttpRequest
from django.db.models.query import QuerySet
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode
from neo4j.exceptions import ServiceUnavailable
from ...errors import NotFound, ConnexionDB


class BaseGenericViewSet(GenericViewSet):
    lookup_field = 'uuid'
    authentication_classes = []
    permission_classes = []

    def __init__(self, serializer_class: Serializer, model_class: StructuredNode, search_field: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class: Serializer = serializer_class
        self.model_class: StructuredNode = model_class
        self.search_field: str = search_field

    def get_nodeset(self) -> NodeSet:
        return self.model_class.nodes

    def get_queryset(self) -> QuerySet:
        queryset: NodeSet = self.get_nodeset()
        request: HttpRequest = self.request
        try:
            if self.search_field:
                search: str = request.GET.get('search', '').strip()
                for term in search.split(','):
                    if term:
                        # Le search field n'étant pas identique,
                        # il est nécessaire de filtrer ainsi
                        queryset = queryset.filter(
                            **{f'{self.search_field}__icontains': term}
                        )
            return queryset.all()
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover
    
    def get_object(self) -> StructuredNode:
        try:
            return self.get_nodeset().get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(self.model_class)
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover
