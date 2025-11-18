from rest_framework import status
from rest_framework.response import Response
from ..views import BaseRelationShipViewSet
from ..models import Interview, Extrait, PositionExtraitRel
from ..serializers import InterviewsSerializer, PositionInputSerializer


class InterviewsViewSet(BaseRelationShipViewSet):
    """
    Renvoie les interviews qui sont connecté à l'extrait
    """
    def __init__(self, **kwargs):
        super().__init__(InterviewsSerializer, Interview, 'extrait_uuid', Extrait, 'APPARTIENT_A', 'titre', **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Modifie position sur la relation APPARTIENT_A.
        """
        serializer_in = PositionInputSerializer(data=request.data)
        serializer_in.is_valid(raise_exception=True)
        new_position = serializer_in.validated_data['position']

        interview: Interview = self.get_object()
        extrait: Extrait = self.get_context_model()
        rel: PositionExtraitRel = extrait.interviews.relationship(interview)
        rel.position = int(new_position)
        rel.save()
        return Response(self.get_serializer(interview, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)
