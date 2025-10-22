from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Interview
from ..serializers import InterviewSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    """
    Renvoie les interviews
    """
    serializer_class = InterviewSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        interviews = Interview.nodes
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return interviews.all()
        for term in search.split():
            if term:
                interviews = interviews.filter(titre__icontains=term)
        return interviews.all()

    def get_object(self):
        try:
            return Interview.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Interview introuvable.', 404)


class ArtisteInterviewViewSet(viewsets.ModelViewSet):
    """
    Renvoie les interviews d'un artiste
    """
    serializer_class = InterviewSerializer
    router_lookup_field = 'artiste_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Interview)-[:PARTICIPER]->(t:Artiste {uuid: $uuid}) RETURN q"
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Interview.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Interview {uuid: $uuid})-[:PARTICIPER]->(t:Artiste {uuid: $artiste}) RETURN q"
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'artiste': self.kwargs[self.router_lookup_field]})[0]
            return Interview.inflate(results[0][0])
        except:
            raise NotFound('Interview introuvable.', 404)


class TagInterviewViewSet(viewsets.ModelViewSet):
    """
    Renvoie les interviews en fonction d'un tag
    """
    serializer_class = InterviewSerializer
    router_lookup_field = 'tag_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Interview)-[:TAGS_INTERVIEW]->(t:Tag {uuid: $uuid}) RETURN q"
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Interview.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Interview {uuid: $uuid})-[:TAGS_INTERVIEW]->(t:Tag {uuid: $tag}) RETURN q"
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'tag': self.kwargs[self.router_lookup_field]})[0]
            return Interview.inflate(results[0][0])
        except:
            raise NotFound('Interview introuvable.', 404)
