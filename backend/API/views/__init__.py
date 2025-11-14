from django.http import HttpRequest
from django.db.models.query import QuerySet
from rest_framework import viewsets, serializers
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode

class Base(viewsets.ModelViewSet):
    """
    Classe de base pour les ModelViewSets classiques
    """
    lookup_field = 'uuid'

    def __init__(self, serializer_class: serializers.Serializer, model_class: StructuredNode, search_field: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class: serializers.Serializer = serializer_class
        self.model_class: StructuredNode = model_class
        self.search_field: str = search_field

    def get_nodeset(self) -> NodeSet:
        # Voir pour les sous endpoints s'il n'est pas possible de build le NodeSet à partir d'une liste de Node
        return self.model_class.nodes

    def get_queryset(self) -> QuerySet:
        queryset: NodeSet = self.get_nodeset()
        request: HttpRequest = self.request
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
    
    def get_object(self) -> StructuredNode:
        try:
            return self.get_nodeset().get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(self.model_class)


class subBase(Base):
    """
    
    """

    def __init__(self, serializer_class, model_class, router_lookup_field, router_model_class, relationship, search_field = None, **kwargs):
        super().__init__(serializer_class, model_class, search_field, **kwargs)
        self.router_lookup_field = router_lookup_field
        self.router_model_class = router_model_class
        self.relationship = relationship

    def get_nodeset(self) -> NodeSet:
        query = "MATCH (q:" + self.model_class.__name__ + ")-[:" + self.relationship + "]->(t:"+ self.router_model_class.__name__ + " {uuid: $uuid}) RETURN q.uuid"
        nodeset = super().get_nodeset().filter(uuid__in=[
                uuid[0] for uuid in db.cypher_query(
                    query, {'uuid': self.kwargs[self.router_lookup_field]}
                )[0]
            ]
        )
        return nodeset


from .theme import *
from .question import *
from .extrait import *
from .interview import *
from .artiste import *
from .utilisateur import *
from .style_musical import *
from .nation import *
from .tag import *
from .style import *
from .recherches_artistes import *
from .regarder_interviews import *
from .regarder_extraits import *
from .recherches_questions import *
from .interviews import *
from .tags_extrait import *
from .tags_interview import *
from .login import *