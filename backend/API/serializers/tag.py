from rest_framework import serializers
from ..models import Tag
from ..serializers import Base


class TagSerializer(Base):
    """
    Sérializer du node Tag
    """

    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Tag, *args, **kwargs)

    def get_interviews(self, tag):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url("interview-list", kwargs={"tag_uuid": tag.uuid})

    def get_extraits(self, tag):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"tag_uuid": tag.uuid})

    def create(self, validated_data):
        """
        Création d'un tag
        """
        return super().create(validated_data)

    def update(self, tag, validated_data):
        """
        Modification d'un tag
        """
        return super().update(tag, validated_data)
