from rest_framework import serializers
from ..serializers import BaseSerializer
from ..models import Audio


class AudioSerializer(BaseSerializer):
    """
    Sérializer du node Audio
    """

    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Outputs
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Audio, *args, **kwargs)

    def get_extraits(self, audio):
        """
        Renvoie un lien propre vers les extraits
        """
        return self.get_url("extrait-list", kwargs={"audio_uuid": audio.uuid})
