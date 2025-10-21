# views.py
from django.urls import reverse
from rest_framework import viewsets
from neomodel import db
from neomodel.exceptions import DoesNotExist
from rest_framework.exceptions import NotFound
from .models import Artiste, Extrait, Interview, Theme, Question, Utilisateur
from .serializers import ArtisteSerializer, ExtraitSerializer, InterviewSerializer, ThemeSerializer, QuestionSerializer, UtilisateurSerializer


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
    router_lookup_field = 'theme_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = """
        MATCH (q:Question)-[:APPARTIENT_A]->(t:Theme {uuid: $uuid})
        RETURN q
        """
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Question.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = """
            MATCH (q:Question {uuid: $uuid})-[:APPARTIENT_A]->(t:Theme {uuid: $theme})
            RETURN q
            """
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs[self.router_lookup_field]})[0]
            return Question.inflate(results[0][0])
        except:
            raise NotFound('Question introuvable.')

class ExtraitViewSet(viewsets.ModelViewSet):
    serializer_class = ExtraitSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Extrait.nodes.all()

    def get_object(self):
        try:
            return Extrait.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Extrait introuvable.')

class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Interview.nodes.all()

    def get_object(self):
        try:
            return Interview.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Interview introuvable.')

class InterviewExtraitViewSet(viewsets.ModelViewSet):
    serializer_class = ExtraitSerializer
    router_lookup_field = 'interview_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = """
        MATCH (q:Extrait)-[:APPARTIENT_A]->(t:Interview {uuid: $uuid})
        RETURN q
        """
        results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
        return [Extrait.inflate(row[0]) for row in results]

    def get_object(self):
        try:
            query = """
            MATCH (q:Extrait {uuid: $uuid})-[:APPARTIENT_A]->(t:Interview {uuid: $theme})
            RETURN q
            """
            results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs[self.router_lookup_field]})[0]
            return Extrait.inflate(results[0][0])
        except:
            raise NotFound('Extrait introuvable.')

class ArtisteViewSet(viewsets.ModelViewSet):
    serializer_class = ArtisteSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Artiste.nodes.all()
    
    def get_object(self):
        try:
            return Artiste.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.')

# class ArtisteInterviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ExtraitSerializer
#     router_lookup_field = 'interview_uuid'
#     lookup_field = 'uuid'

#     def get_queryset(self):
#         query = """
#         MATCH (q:Extrait)-[:APPARTIENT_A]->(t:Interview {uuid: $uuid})
#         RETURN q
#         """
#         results, _ = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})
#         return [Extrait.inflate(row[0]) for row in results]

#     def get_object(self):
#         try:
#             query = """
#             MATCH (q:Extrait {uuid: $uuid})-[:APPARTIENT_A]->(t:Interview {uuid: $theme})
#             RETURN q
#             """
#             results = db.cypher_query(query, {'uuid': self.kwargs[self.lookup_field], 'theme': self.kwargs[self.router_lookup_field]})[0]
#             return Extrait.inflate(results[0][0])
#         except:
#             raise NotFound('Extrait introuvable.')

class UtilisateurViewSet(viewsets.ModelViewSet):
    serializer_class = UtilisateurSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Utilisateur.nodes.all()
    
    def get_object(self):
        try:
            return Utilisateur.nodes.get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound('Utilisateur introuvable.')