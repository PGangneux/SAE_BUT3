from neomodel import db
from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import StyleMusical
from ..serializers import StyleMusicalSerializer


class StyleMusicalViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes
    """
    serializer_class = StyleMusicalSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return StyleMusical.nodes.all()
    
    def get_object(self):
        try:
            return StyleMusical.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.', 404)

class ArtisteStyleMusicalViewSet(viewsets.ModelViewSet):
    """
    Renvoie les styles musicaux de l'artiste
    """
    serializer_class = StyleMusicalSerializer
    router_lookup_field = 'artiste_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:StyleMusical)<-[:STYLE]-(t:Artiste {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [StyleMusical.inflate(row[0]) for row in results]
    
    def get_object(self):
        try:
            query = "MATCH (q:StyleMusical {uuid: $uuid})<-[:STYLE]-(t:Artiste {uuid: $artiste}) RETURN q"
            results = db.cypher_query(query, {'artiste': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return StyleMusical.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Style Musical introuvable.', 404)
