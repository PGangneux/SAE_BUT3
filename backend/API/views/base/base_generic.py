from django.http import HttpRequest
from django.db.models.query import QuerySet
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet, RawCypher
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
        """Récupère le nodeset de la view, même chose qu'un queryset mais pour neomodel

        Returns:
            NodeSet: ensemble de structurenode du modèle
        """
        return self.model_class.nodes

    def get_queryset(self) -> QuerySet:
        """Récupère le queryset de la view

        Raises:
            ConnexionDB: La base de données n'est pas disponible

        Returns:
            QuerySet: queryset filtrer et ordonner
        """
        queryset: NodeSet = self.get_nodeset()
        request: HttpRequest = self.request
        # Recherche (search)
        if self.search_field:
            queryset = self.search_nodeset(queryset, request.GET.get('search', '').strip())
        # Ordonne (order)
        order = request.GET.get('order', '').strip()
        if order != '':
            queryset = self.order_nodeset(queryset, order)
        try:
            return queryset.all()
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover
    
    def get_object(self) -> StructuredNode:
        """Récupère l'objet dans le nodeset

        Raises:
            NotFound: L'objet rechercher n'a pas été trouvé
            ConnexionDB: La base de données n'est pas disponnible

        Returns:
            StructuredNode: Intance rechercher
        """
        try:
            return self.get_nodeset().get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(self.model_class)
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover
    
    def search_nodeset(self, nodeset: NodeSet, search: str) -> NodeSet:
        """Filtre le nodeset en fonction de la recherche

        Args:
            nodeset (NodeSet): nodeset dans lequel on effectue la recherche
            search (str): champ recherche

        Returns:
            NodeSet: nodeset filtré
        """
        for term in search.split(','):
            if term:
                # Le search field n'étant pas identique pour tous les models,
                # il est nécessaire de filtrer ainsi
                nodeset = nodeset.filter(**{f'{self.search_field}__icontains': term})
        return nodeset

    def order_nodeset(self, nodeset: NodeSet, order: str) -> NodeSet:
        """Ordonne le nodeset en fonction du champ renseigner

        Args:
            nodeset (NodeSet): nodeset que l'on ordonne
            order (str): champ sur lequel on ordonne

        Returns:
            NodeSet: nodeset ordonné
        """
        ordering = []
        for term in order.split(','):
            if '__' in term:
                # En cas de relationship ou/et field non présent,
                # erreur non fatal dans le terminal
                # ($n)-[r:relationship]-(s) pour ne pas se soucier du sens de la relation
                field_list = term.split('__')

                # Sens de l'ordre
                sens = "DESC" if field_list[0][0] == "-" else "ASC"
                if sens == "DESC": field_list[0] = field_list[0][1:]

                # Dernière relation
                relationship = field_list[-2]

                # Field d'ordering
                field = field_list[-1]
                
                # Ordonner le queryset
                ord = "head([($n)"
                for i in range(len(field_list)-2):
                    ord += f"-[:{field_list[i].upper()}]{"-()" if i < len(field_list)-2 else ""}"
                ord += f"-[r:{relationship.upper()}]-(s) | s.{field}]) {sens}"
                ordering.append(
                    RawCypher(
                        ord
                    )
                )

            elif '|' in term:
                # En cas de relationship ou/et field non présent,
                # erreur non fatal dans le terminal
                # Prévoir une situtation où la relation et/ou le field n'existe pas
                # Prévoir une solution où plus d'un |
                relationship, field = term.split('|')
                sens = "DESC" if relationship[0] == "-" else "ASC"
                if sens == "DESC":
                    relationship = relationship[1:]
                ordering.append(
                    RawCypher(
                        # ($n)-[r:relationship]-(s) pour ne pas se soucier du sens de la relation
                        f"head([($n)-[r:{relationship.upper()}]-(s) | r.{field}]) {sens}"
                    )
                )

            else:
                # Fonctionnement classique.
                ordering.append(term)
        return nodeset.order_by(*ordering)
