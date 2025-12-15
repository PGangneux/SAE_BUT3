from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode, db
from neo4j.exceptions import ServiceUnavailable
from ...errors import NotFound, ConnexionDB
from ..base import BaseGenericViewSet


class BaseRelationShipViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, BaseGenericViewSet):
    """
    Classe de base pour les ModelViewSets des relations
    """
    def __init__(
            self, serializer_class: Serializer, model_class: StructuredNode,
            router_lookup_field: str, router_model_class: StructuredNode,
            relationship: str, search_field: str = None, **kwargs
    ):
        super().__init__(serializer_class, model_class, search_field, **kwargs)
        self.router_lookup_field: str = router_lookup_field
        self.router_model_class: StructuredNode = router_model_class
        self.relationship: str = relationship
    def get_nodeset(self) -> NodeSet:
        try:
            router_nodeset: NodeSet = self.router_model_class.nodes
            router_nodeset.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound(self.router_model_class)
        query: str = "MATCH (q:" + str(self.model_class.__name__) + ")-[r:" + self.relationship + "]-\
            (t:" + str(self.router_model_class.__name__) + " {uuid: $uuid}) RETURN q.uuid"
        nodeset: NodeSet = self.model_class.nodes
        try:
            nodeset = nodeset.filter(
                uuid__in=[
                    uuid[0] for uuid in db.cypher_query(
                        query, {'uuid': self.kwargs[self.router_lookup_field]}
                    )[0]
                ]
            )
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover
        return nodeset
    
    def get_context_model(self) -> StructuredNode:
        """
        Récupère le node router
        """
        try:
            router_nodeset: NodeSet = self.router_model_class.nodes
            return router_nodeset.get(uuid=self.kwargs[self.router_lookup_field])
        # N'est jamais sensé passer pas ici, raise déjà dans get_nodeset
        except DoesNotExist: # pragma: no cover
            raise NotFound(self.router_model_class) # pragma: no cover
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover

    def get_serializer_context(self):
        """
        Modification du contexte du sérializer
        """
        context = super().get_serializer_context()
        context_model_name: str = self.router_model_class.__name__
        context[context_model_name.lower()] = self.get_context_model()
        return context

    def perform_destroy(self, instance):
        """
        Suppression de la RelationShip
        """
        context_model_name: str = self.router_model_class.__name__
        serializer = self.get_serializer(
            context={
                context_model_name.lower(): self.get_context_model()
            }
        )
        serializer.delete(instance.uuid)

    def create(self, request, *args, **kwargs):
        """
        Création de la RelationShip
        """
        data = request.data
        context_model_name: str = self.router_model_class.__name__
        serializer: Serializer = self.serializer_class(
            data=data,
            context={
                context_model_name.lower(): self.get_context_model()
            }
        )
        serializer.is_valid()
        instance = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(instance, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
