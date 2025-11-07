from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from ..errors import NotFound
from ..models import Question
from ..serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Renvoie les question
    """
    serializer_class = QuestionSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        questions = Question.nodes
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return questions.all()
        for term in search.split():
            if term:
                questions = questions.filter(texte__icontains=term)
        return questions.all()

    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            return Question.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(Question)


class ThemeQuestionViewSet(viewsets.ModelViewSet):
    """
    Renvoie les questions qui appartiennent à un thème
    """
    serializer_class = QuestionSerializer
    router_lookup_field = 'theme_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        query = "MATCH (q:Question)-[:A_THEME]->(t:Theme {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Question.inflate(row[0]) for row in results]

    def get_object(self):
        """
        Récupération de l'Objet
        """
        query = "MATCH (q:Question {uuid: $uuid})-[:A_THEME]->(t:Theme {uuid: $theme}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs[self.router_lookup_field]})[0]
        if not results:
            raise NotFound(Question)
        return Question.inflate(results[0][0])