from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Question
from ..serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Renvoie les question
    """
    serializer_class = QuestionSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        questions = Question.nodes
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return questions.all()
        for term in search.split():
            if term:
                questions = questions.filter(texte__icontains=term)
        return questions.all()

    def get_object(self):
        try:
            return Question.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Question introuvable.', 404)


class ThemeQuestionViewSet(viewsets.ModelViewSet):
    """
    Renvoie les questions qui appartiennent à un thème
    """
    serializer_class = QuestionSerializer
    router_lookup_field = 'theme_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Question)-[:A_THEME]->(t:Theme {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Question.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = "MATCH (q:Question {uuid: $uuid})-[:A_THEME]->(t:Theme {uuid: $theme}) RETURN q"
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs[self.router_lookup_field]})[0]
            return Question.inflate(results[0][0])
        except:
            raise NotFound('Question introuvable.', 404)


class UtilisateurQuestionViewSet(viewsets.ModelViewSet):
    """
    Renvoie les questions qui ont été recherché par l'utilisateur
    """
    serializer_class = QuestionSerializer
    router_lookup_field = 'utilisateur_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Question)<-[:RECHERCHES_QUESTIONS]-(t:Utilisateur {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Question.inflate(row[0]) for row in results]
    
    def get_object(self):
        try:
            query = "MATCH (q:Question {uuid: $uuid})<-[:RECHERCHES_QUESTIONS]-(t:Utilisateur {uuid: $utilisateur}) RETURN q"
            results = db.cypher_query(query, {'utilisateur': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Question.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Question introuvable.', 404)
