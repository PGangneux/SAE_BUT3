from rest_framework.serializers import Serializer
from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode, db
from neo4j.exceptions import ServiceUnavailable
from ...errors import NotFound, ConnexionDB
from ..base import BaseModelViewSet


class SubBaseModelViewSet(BaseModelViewSet):
    """
    Classe de base pour les ModelViewSets de sous endpoints
    """
    def __init__(
            self, serializer_class: Serializer, model_class: StructuredNode,
            router_lookup_field: str, router_model_class: StructuredNode,
            relationship: str, search_field: str = None, ordered_by: str = None, **kwargs
    ):
        super().__init__(serializer_class, model_class, search_field, **kwargs)
        self.router_lookup_field: str = router_lookup_field
        self.router_model_class: StructuredNode = router_model_class
        self.relationship: str = relationship
        self.ordered_by: str = ordered_by

    def get_nodeset(self) -> NodeSet:
        try:
            router_nodeset: NodeSet = self.router_model_class.nodes
            router_nodeset.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound(self.router_model_class)
        query: str = "MATCH (q:" + str(self.model_class.__name__) + ")-[r:" + self.relationship + "]-\
            (t:" + str(self.router_model_class.__name__) + " {uuid: $uuid}) RETURN q.uuid"
        if self.ordered_by:
            query += " order by " + self.ordered_by
        try:
            nodeset: NodeSet = super().get_nodeset().filter(
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