from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Extrait
from ..serializers import ExtraitSerializer


class ExtraitViewSet(viewsets.ModelViewSet):
    """
    Renvoie les extraits
    """
    serializer_class = ExtraitSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Extrait.nodes.all()

    def get_object(self):
        try:
            return Extrait.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Extrait introuvable.', 404)


class QuestionExtraitViewSet(viewsets.ModelViewSet):
    """
    Renvoie les extraits qui répondent à la question
    """
    serializer_class = ExtraitSerializer
    router_lookup_field = 'question_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Extrait)-[:POSE]->(t:Question {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Extrait.inflate(row[0]) for row in results]

    def get_object(self):
        query = "MATCH (q:Extrait {uuid: $uuid})-[:POSE]->(t:Question {uuid: $question}) RETURN q"
        results = db.cypher_query(query, {'question': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
        return Extrait.inflate(results[0][0])


class InterviewExtraitViewSet(viewsets.ModelViewSet):
    """
    Renvoie les extraits qui appartiennent à une interview
    """
    serializer_class = ExtraitSerializer
    router_lookup_field = 'interview_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Extrait)-[:APPARTIENT_A]->(t:Interview {uuid: $uuid}) RETURN q"
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Extrait.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Extrait {uuid: $uuid})-[:APPARTIENT_A]->(t:Interview {uuid: $theme}) RETURN q"
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs[self.router_lookup_field]})[0]
            return Extrait.inflate(results[0][0])
        except:
            raise NotFound('Extrait introuvable.', 404)


class TagExtraitViewSet(viewsets.ModelViewSet):
    """
    Renvoie les extraits en fonction d'un tag
    """
    serializer_class = ExtraitSerializer
    router_lookup_field = 'tag_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Extrait)-[:TAGS_EXTRAIT]->(t:Tag {uuid: $uuid}) RETURN q"
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Extrait.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Extrait {uuid: $uuid})-[:TAGS_EXTRAIT]->(t:Tag {uuid: $tag}) RETURN q"
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'tag': self.kwargs[self.router_lookup_field]})[0]
            return Extrait.inflate(results[0][0])
        except:
            raise NotFound('Extrait introuvable.', 404)

