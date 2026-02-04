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
        self,
        serializer_class: Serializer,
        model_class: StructuredNode,
        router_lookup_field: str,
        router_model_class: StructuredNode,
        relationship: str,
        search_field: str = None,
        ordered_by: str = None,
        **kwargs,
    ):
        """Classe de base pour les ModelViewSets de sous endpoints

        Args:
            serializer_class (Serializer): Serializer du ViewSet
            model_class (StructuredNode): type de node du ViewSet
            router_lookup_field (str): nom du champ à récupérer dans l'url pour avoir le node de context
            router_model_class (StructuredNode): type de node du context du ViewSet
            relationship (str): nom de la relation entre le node et le node de context
            search_field (str, optional): Champ utiliser pour la recherche si fourni. Defaults to None.
            ordered_by (str, optional): Champ utiliser pour ordonner le queryset par défaut. Defaults to None.
        """
        super().__init__(serializer_class, model_class, search_field, **kwargs)
        self.router_lookup_field: str = router_lookup_field
        self.router_model_class: StructuredNode = router_model_class
        self.relationship: str = relationship
        self.ordered_by: str = ordered_by

    def get_nodeset(self) -> NodeSet:
        try:
            # Vérifie que l'instance du router existe bien
            self.router_model_class.nodes.get(
                uuid=self.kwargs[self.router_lookup_field]
            )
            return (
                super()
                .get_nodeset()
                .filter(
                    uuid__in=[
                        uuid[0]
                        for uuid in db.cypher_query(
                            # Requête CYPHER
                            f"MATCH (n:{self.model_class.__name__})-[r:{self.relationship}]-\
                        (:{str(self.router_model_class.__name__)} "
                            + "{uuid: $uuid}) RETURN n.uuid" + (f" ORDER BY {self.ordered_by} DESC" if self.ordered_by else ""),
                            {"uuid": self.kwargs[self.router_lookup_field]},
                        )[0]
                    ]
                )
            )
        except DoesNotExist:
            raise NotFound(self.router_model_class)
        # Dans le cas ou la base de données est inaccessible
        except ServiceUnavailable:  # pragma: no cover
            raise ConnexionDB()  # pragma: no cover
