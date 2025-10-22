from neomodel import db
from rest_framework import viewsets
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Tag
from ..serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    Renvoie les tags
    """
    serializer_class = TagSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Tag.nodes.all()

    def get_object(self):
        try:
            return Tag.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Thème introuvable.', 404)

class InterviewTagViewSet(viewsets.ModelViewSet):
    """
    Renvoie les tags d'une interview
    """
    serializer_class = TagSerializer
    router_lookup_field = 'interview_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Tag)<-[:TAGS_INTERVIEW]-(t:Interview {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Tag.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Tag {uuid: $uuid})<-[:TAGS_INTERVIEW]-(t:Interview {uuid: $interview}) RETURN q"
            results = db.cypher_query(query, {'interview': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Tag.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Tag introuvable.', 404)

class ExtraitTagViewSet(viewsets.ModelViewSet):
    """
    Renvoie les tags d'un extrait
    """
    serializer_class = TagSerializer
    router_lookup_field = 'extrait_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Tag)<-[:TAGS_EXTRAIT]-(t:Extrait {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Tag.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Tag {uuid: $uuid})<-[:TAGS_EXTRAIT]-(t:Extrait {uuid: $extrait}) RETURN q"
            results = db.cypher_query(query, {'extrait': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Tag.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Tag introuvable.', 404)
