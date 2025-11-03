from django.urls import reverse
from rest_framework import serializers
from ..models import Tag

class TagsExtraitRelationShipSerializer(serializers.Serializer):
    """
    Sérializer RelationShip tags_extrait (Extrait <-> Tag)
    """
    uuid = serializers.CharField(required=True)
    name = serializers.CharField(read_only=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def get_interviews(self, tag):
        """
        Renvoie un lien propre vers les interviews :
        """
        return {"url": self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'tag_uuid': tag.uuid}))}

    def get_extraits(self, tag):
        """
        Renvoie un lien propre vers les extraits :
        """
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'tag_uuid': tag.uuid}))}

    def create(self, validated_data):
        """
        Connecte un tag à un extrait
        """
        extrait = self.context.get('extrait')
        if not extrait:
            raise serializers.ValidationError("Extrait manquant dans le contexte.")

        tag_uuid = validated_data['uuid']
        try:
            tag = Tag.nodes.get(uuid=tag_uuid)
        except Tag.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Tag introuvable.'})

        if not extrait.tags_extrait.is_connected(tag):
            extrait.tags_extrait.connect(tag)

        return tag

    def delete(self, tag_uuid):
        """
        Déconnecte un tag d’un extrait
        """
        extrait = self.context.get('extrait')
        if not extrait:
            raise serializers.ValidationError("Extrait manquant dans le contexte.")

        try:
            tag = Tag.nodes.get(uuid=tag_uuid)
        except Tag.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Tag introuvable.'})

        extrait.tags_extrait.disconnect(tag)
        return tag
