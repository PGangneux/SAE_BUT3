from rest_framework import serializers
from ..serializers import BaseSerializer
from ..models import Occasion


class OccasionSerializer(BaseSerializer):
    """
    Sérializer du node Occasion
    """

    name = serializers.CharField(required=True)

    # Output
    interviews = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Occasion, *args, **kwargs)

    def get_interviews(self, occasion: Occasion):
        """
        Renvoie un lien propre vers les interviews
        """
        return self.get_url("interview-list", kwargs={"occasion_uuid": occasion.uuid})
