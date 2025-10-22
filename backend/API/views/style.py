from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Artiste, StyleMusical
from ..serializers import StyleRelationShipSerializer
from neomodel import db, DoesNotExist

class ArtisteStyleRelationShipViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = StyleRelationShipSerializer
    lookup_field = 'uuid'
    router_lookup_field = 'artiste_uuid'

    def get_queryset(self):
        artiste = self.get_artiste()
        query = "MATCH (s:StyleMusical)<-[:STYLE]-(a:Artiste {uuid: $uuid}) RETURN s"
        results = db.cypher_query(query, {'uuid': artiste.uuid})[0]
        return [StyleMusical.inflate(row[0]) for row in results]
    
    def get_object(self):
        try: 
            query = "MATCH (q:StyleMusical {uuid: $uuid})<-[:STYLE]-(t:Artiste {uuid: $artiste}) RETURN q"
            results = db.cypher_query(query, {'artiste': self.kwargs['artiste_uuid'], 'uuid': self.kwargs[self.lookup_field]})[0]
            return StyleMusical.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Style Musical introuvable.', 404)

    def get_artiste(self):
        try:
            return Artiste.nodes.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound('Artiste introuvable.')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['artiste'] = self.get_artiste()
        return context

    def perform_destroy(self, instance):
        serializer = self.get_serializer(context={'artiste': self.get_artiste()})
        serializer.delete(instance.uuid)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'artiste': self.get_artiste()})
        serializer.is_valid(raise_exception=True)
        style = serializer.create(serializer.validated_data)
        return Response({
            'uuid': style.uuid,
            'name': style.name
        }, status=status.HTTP_201_CREATED)
