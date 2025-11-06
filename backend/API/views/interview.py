from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from ..errors import NotFound
from ..models import Interview
from ..serializers import InterviewSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    """
    Renvoie les interviews
    """
    serializer_class = InterviewSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        interviews = Interview.nodes
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return interviews.all()
        for term in search.split():
            if term:
                interviews = interviews.filter(titre__icontains=term)
        return interviews.all()

    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return Interview.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(Interview)


class TagInterviewViewSet(viewsets.ModelViewSet):
    """
    Renvoie les interviews en fonction d'un tag
    """
    serializer_class = InterviewSerializer
    router_lookup_field = 'tag_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        query = "MATCH (q:Interview)-[:TAGS_INTERVIEW]->(t:Tag {uuid: $uuid}) RETURN q"
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Interview.inflate(row[0]) for row in results]

    def get_object(self):
        """
        Récupération de l'Objet
        """
        
        query = "MATCH (q:Interview {uuid: $uuid})-[:TAGS_INTERVIEW]->(t:Tag {uuid: $tag}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'tag': self.kwargs[self.router_lookup_field]})[0]
        if not results:
            raise NotFound(Interview)
        return Interview.inflate(results[0][0])

