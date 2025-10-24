from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..models import Interview, Extrait
from ..serializers import InterviewsSerializer, PositionInputSerializer


class InterviewsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Renvoie les interviews qui sont connecté à l'extrait
    """
    serializer_class = InterviewsSerializer
    router_lookup_field = 'extrait_uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Récupération du QuerySet
        """
        query = "MATCH (q:Interview)<-[:APPARTIENT_A]-(t:Extrait {uuid: $uuid}) RETURN q"
        results = db.cypher_query(query, {'uuid': self.kwargs[self.router_lookup_field]})[0]
        return [Interview.inflate(row[0]) for row in results]
    
    def get_object(self):
        """
        Récupération de l'Objet
        """
        try:
            query = "MATCH (q:Interview {uuid: $uuid})<-[:APPARTIENT_A]-(t:Extrait {uuid: $extrait}) RETURN q"
            results = db.cypher_query(query, {'extrait': self.kwargs[self.router_lookup_field], 'uuid': self.kwargs[self.lookup_field]})[0]
            return Interview.inflate(results[0][0])
        except DoesNotExist:
            raise NotFound('Interview introuvable.', 404)

    def get_extrait(self):
        """
        Récupération de l'extrait
        """
        try:
            return Extrait.nodes.get(uuid=self.kwargs[self.router_lookup_field])
        except DoesNotExist:
            raise NotFound('Extrait introuvable.')

    def get_serializer_context(self):
        """
        Modification du contexte du sérializer
        """
        context = super().get_serializer_context()
        context['extrait'] = self.get_extrait()
        return context

    def perform_destroy(self, instance):
        """
        Suppression de la RelationShip
        """
        serializer = self.get_serializer(context={'extrait': self.get_extrait()})
        serializer.delete(instance.uuid)

    def create(self, request, *args, **kwargs):
        """
        Création de la RelationShip
        """
        serializer = self.get_serializer(data=request.data, context={'extrait': self.get_extrait()})
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(instance, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Modifie position sur la relation APPARTIENT_A.
        """
        serializer_in = PositionInputSerializer(data=request.data)
        serializer_in.is_valid(raise_exception=True)
        new_position = serializer_in.validated_data['position']

        interview = self.get_object()
        rel = self.get_extrait().interviews.relationship(interview)
        if not rel:
            return Response({'detail': "Relation inexistante entre l'extrait et l'interview."}, status=status.HTTP_404_NOT_FOUND)
        try:
            rel.position = int(new_position)
            rel.save()
        except Exception as e:
            return Response({'detail': f'Impossible de mettre à jour la position : {e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(interview, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)