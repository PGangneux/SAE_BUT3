from rest_framework import serializers
from ..models import Tag

class TagsExtraitShipSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True)
    name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """Connecte un tag à un extrait"""
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
        """Déconnecte un tag d’un extrait"""
        extrait = self.context.get('extrait')
        if not extrait:
            raise serializers.ValidationError("Extrait manquant dans le contexte.")

        try:
            tag = Tag.nodes.get(uuid=tag_uuid)
        except Tag.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Tag introuvable.'})

        extrait.tags_extrait.disconnect(tag)
        return tag
