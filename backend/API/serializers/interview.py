from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from ..serializers import BaseSerializer
from ..models import Interview, Occasion
from ..errors import NotFound


class InterviewSerializer(BaseSerializer):
    """
    Sérializer du node Interview
    """

    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    # Input
    occasion_uuid = serializers.CharField(
        write_only=True,
        required=False,
    )

    # Outputs
    occasion = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Interview, *args, **kwargs)

    def get_occasion(self, interview):
        """
        Renvoie un lien propre vers l'occasion
        """
        occasion = interview.occasion.single()
        return (
            self.get_url("occasion-detail", kwargs={"uuid": occasion.uuid})
            if occasion
            else None
        )

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

    def create(self, validated_data):
        """
        Création d'une interview
        """
        occasion_uuid = validated_data.pop("occasion_uuid", None)
        interview = super().create(validated_data)
        if occasion_uuid is not None:
            try:
                interview.occasion.connect(Occasion.nodes.get(uuid=occasion_uuid))
            except DoesNotExist:
                raise NotFound(Occasion)
        return interview

    def update(self, interview, validated_data):
        """
        Modification d'un artiste
        """
        occasion_uuid = validated_data.pop("occasion_uuid", None)
        interview = super().update(interview, validated_data)
        if occasion_uuid is not None:
            try:
                if interview.occasion:
                    interview.occasion.disconnect(interview.occasion.single())
                interview.occasion.connect(Occasion.nodes.get(uuid=occasion_uuid))
            except DoesNotExist:
                raise NotFound(Occasion)
        return interview.save()
