from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..models import Interview, Utilisateur
from ..serializers import RegarderInterviewsSerializer


class RegarderInterviewsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Renvoie les interviews qui ont été regardé par l'utilisateur
    """
    serializer_class = RegarderInterviewsSerializer
    router_lookup_field = 'utilisateur_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        query = "MATCH (q:Interview)<-[:REGARDER_INTERVIEWS]-(t:Utilisateur {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Interview.inflate(row[0]) for row in results]
    
    def get_object(self):
        try:
            query = "MATCH (q:Interview {uuid: $uuid})<-[:REGARDER_INTERVIEWS]-(t:Utilisateur {uuid: $utilisateur}) RETURN q"
            results = db.cypher_query(query, {'utilisateur': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Interview.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Interview introuvable.', 404)

    def get_utilisateur(self):
        try:
            return Utilisateur.nodes.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound('Utilisateur introuvable.')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['utilisateur'] = self.get_utilisateur()
        return context

    def perform_destroy(self, instance):
        serializer = self.get_serializer(context={'utilisateur': self.get_utilisateur()})
        serializer.delete(instance.uuid)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'utilisateur': self.get_utilisateur()})
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(instance, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)