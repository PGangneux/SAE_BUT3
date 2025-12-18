from rest_framework import serializers
from ..serializers import BaseRelationShipSerializer
from ..models import Extrait, Interview


class InterviewsSerializer(BaseRelationShipSerializer):
    """
    Sérializer RelationShip interviews (Extrait <-> Interview)
    """

    position = serializers.IntegerField(write_only=True, required=True)

    # Outputs
    titre = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    occasion = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    lieu = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    lieu = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Interview, Extrait, "interviews", *args, **kwargs)

    def get_extraits(self, interview):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"interview_uuid": interview.uuid})

    def get_tags(self, interview):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url("tag-list", kwargs={"interview_uuid": interview.uuid})


class PositionInputSerializer(serializers.Serializer):
    """
    Sérializer RelationShip interviews (Extrait <-> Interview) update
    """

    position = serializers.IntegerField(write_only=True, required=True)
