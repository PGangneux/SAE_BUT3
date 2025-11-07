from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..errors import NotFound
from ..models import Artiste
from ..serializers import ArtisteSerializer


class ArtisteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes
    """
    serializer_class = ArtisteSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        artistes = Artiste.nodes
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return artistes.all()
        for term in search.split():
            if term:
                artistes = artistes.filter(name__icontains=term)
        return artistes.all()
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return Artiste.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(Artiste)


class StyleMusicalArtisteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes en fonction d'un style musical
    """
    serializer_class = ArtisteSerializer
    router_lookup_field = 'stylemusical_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        query = "MATCH (q:Artiste)-[:STYLE]->(t:StyleMusical {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Artiste.inflate(row[0]) for row in results]
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        query = "MATCH (q:Artiste {uuid: $uuid})-[:STYLE]->(t:StyleMusical {uuid: $stylemusical}) RETURN q"
        results = db.cypher_query(query, {'stylemusical': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
        if not results:
            raise NotFound(Artiste)
        return Artiste.inflate(results[0][0])


class NationArtisteViewSet(viewsets.ModelViewSet):
    """
    Renvoie les artistes en fonction de leur nationnalite
    """
    serializer_class = ArtisteSerializer
    router_lookup_field = 'nation_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        query = "MATCH (q:Artiste)-[:NATIONALITE]->(t:Nation {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Artiste.inflate(row[0]) for row in results]
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        query = "MATCH (q:Artiste {uuid: $uuid})-[:NATIONALITE]->(t:Nation {uuid: $nation}) RETURN q"
        results = db.cypher_query(query, {'nation': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
        if not results:
            raise NotFound(Artiste)
        return Artiste.inflate(results[0][0])
