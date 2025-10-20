# views.py
from django.urls import reverse
from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from .models import Theme, Question
from .serializers import ThemeSerializer, QuestionSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Theme.nodes.all()

    def get_object(self):
        try:
            return Theme.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Thème introuvable.')

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Question.nodes.all()

    def get_object(self):
        try:
            return Question.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Question introuvable.')
        

class ThemeQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        query = """
        MATCH (q:Question)-[:APPARTIENT_A]->(t:Theme {uuid: $uuid})
        RETURN q
        """
        results, _ = db.cypher_query(query, {'uuid': self.kwargs["theme_uuid"]})
        return [Question.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = """
            MATCH (q:Question {uuid: $uuid})-[:APPARTIENT_A]->(t:Theme {uuid: $theme})
            RETURN q
            """
            results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs["theme_uuid"]})
            return Question.inflate(results[0][0])
        except:
            raise NotFound('Question introuvable.')
