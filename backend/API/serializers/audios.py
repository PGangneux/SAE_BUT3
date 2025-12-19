from rest_framework import serializers
from ..serializers import BaseRelationShipSerializer
from ..models import Extrait, Audio


class AudiosSerializer(BaseRelationShipSerializer):
    """
    Sérializer RelationShip audios (Extrait <-> Audio)
    """

    # Outputs
    name = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Audio, Extrait, "audios", *args, **kwargs)

    def get_extraits(self, audio: Audio):
        """
        Renvoie un lien propre vers les extraits
        """
        return self.get_url("extrait-list", kwargs={"audio_uuid": audio.uuid})
