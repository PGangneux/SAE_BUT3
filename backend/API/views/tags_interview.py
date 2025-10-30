from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Interview, Tag
from ..serializers import TagsInterviewRelationShipSerializer
from neomodel import db, DoesNotExist

class TagsInterviewRelationShipViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TagsInterviewRelationShipSerializer
    router_lookup_field = 'interview_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        interview = self.get_interview()
        query = "MATCH (s:Tag)<-[:TAGS_INTERVIEW]-(a:Interview {uuid: $uuid}) RETURN s"
        results = db.cypher_query(query, {'uuid': interview.uuid})[0]
        return [Tag.inflate(row[0]) for row in results]
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            query = "MATCH (q:Tag {uuid: $uuid})<-[:TAGS_INTERVIEW]-(t:Interview {uuid: $interview}) RETURN q"
            results = db.cypher_query(query, {'interview': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Tag.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Tag introuvable.', 404)

    def get_interview(self):
        """
        Récupération de l'interview
        """
        try:
            return Interview.nodes.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound('Interview introuvable.')

    def get_serializer_context(self):
        """
        Modification du contexte du sérializer
        """
        context = super().get_serializer_context()
        context['interview'] = self.get_interview()
        return context

    def perform_destroy(self, instance):
        """
        Suppression de la RelationShip
        """
        serializer = self.get_serializer(context={'interview': self.get_interview()})
        serializer.delete(instance.uuid)

    def create(self, request, *args, **kwargs):
        """
        Création de la RelationShip
        """
        serializer = self.get_serializer(data=request.data, context={'interview': self.get_interview()})
        serializer.is_valid(raise_exception=True)
        tag = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(tag, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
