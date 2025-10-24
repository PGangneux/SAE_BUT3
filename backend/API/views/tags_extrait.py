from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Extrait, Tag
from ..serializers import TagsExtraitShipSerializer
from neomodel import db, DoesNotExist

class TagsExtraitRelationShipViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TagsExtraitShipSerializer
    router_lookup_field = 'extrait_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        extrait = self.get_extrait()
        query = "MATCH (s:Tag)<-[:TAGS_EXTRAIT]-(a:Extrait {uuid: $uuid}) RETURN s"
        results = db.cypher_query(query, {'uuid': extrait.uuid})[0]
        print(results)
        return [Tag.inflate(row[0]) for row in results]
    
    def get_object(self):
        try:
            query = "MATCH (q:Tag {uuid: $uuid})<-[:TAGS_EXTRAIT]-(t:Extrait {uuid: $extrait}) RETURN q"
            results = db.cypher_query(query, {'extrait': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Tag.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Tag introuvable.', 404)

    def get_extrait(self):
        try:
            return Extrait.nodes.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound('Extrait introuvable.')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['extrait'] = self.get_extrait()
        return context

    def perform_destroy(self, instance):
        serializer = self.get_serializer(context={'extrait': self.get_extrait()})
        serializer.delete(instance.uuid)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'extrait': self.get_extrait()})
        serializer.is_valid(raise_exception=True)
        tag = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(tag, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
