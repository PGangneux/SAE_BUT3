from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from neomodel import db
from rest_framework.exceptions import NotFound
from ..models import Artiste
from ..serializers import ArtisteSerializer


class ArtisteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes
    """
    serializer_class = ArtisteSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Artiste.nodes.all()
    
    def get_object(self):
        try:
            return Artiste.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.', 404)


class StyleMusicalArtisteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes en fonction d'un style musical
    """
    serializer_class = ArtisteSerializer
    router_lookup_field = 'stylemusical_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Artiste)-[:STYLE]->(t:StyleMusical {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Artiste.inflate(row[0]) for row in results]
    
    def get_object(self):
        try:
            query = "MATCH (q:Artiste {uuid: $uuid})-[:STYLE]->(t:StyleMusical {uuid: $stylemusical}) RETURN q"
            results = db.cypher_query(query, {'stylemusical': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Artiste.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.', 404)
