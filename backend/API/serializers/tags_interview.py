from django.urls import reverse
from rest_framework import serializers
from ..models import Tag

class TagsInterviewRelationShipSerializer(serializers.Serializer):
    """
    Sérializer RelationShip tags_interview (Interview <-> Tag)
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
        Connecte un tag à un interview
        """
        interview = self.context.get('interview')
        if not interview:
            raise serializers.ValidationError("Interview manquant dans le contexte.")

        tag_uuid = validated_data['uuid']
        try:
            tag = Tag.nodes.get(uuid=tag_uuid)
        except Tag.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Tag introuvable.'})

        if not interview.tags_interview.is_connected(tag):
            interview.tags_interview.connect(tag)

        return tag

    def delete(self, tag_uuid):
        """
        Déconnecte un tag d’un interview
        """
        interview = self.context.get('interview')
        if not interview:
            raise serializers.ValidationError("Interview manquant dans le contexte.")

        try:
            tag = Tag.nodes.get(uuid=tag_uuid)
        except Tag.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Tag introuvable.'})

        interview.tags_interview.disconnect(tag)
        return tag
