from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..views import Base, subBase
from ..errors import NotFound
from ..models import Artiste, Nation
from ..serializers import ArtisteSerializer


class ArtisteViewSet(Base):
    """
    Renvoie les artistes
    """
    
    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, 'name', **kwargs)


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


class NationArtisteViewSet(subBase):
    """
    Renvoie les artistes en fonction de leur nationnalite
    """
    
    def __init__(self, **kwargs):
        super().__init__(ArtisteSerializer, Artiste, 'nation_uuid', Nation, 'NATIONALITE', 'name', **kwargs)
