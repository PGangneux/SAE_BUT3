from rest_framework import serializers
from ..models import StyleMusical

class StyleRelationShipSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True)
    name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """Connecte un style à un artiste"""
        artiste = self.context.get('artiste')
        if not artiste:
            raise serializers.ValidationError("Artiste manquant dans le contexte.")

        style_uuid = validated_data['uuid']
        try:
            style = StyleMusical.nodes.get(uuid=style_uuid)
        except StyleMusical.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Style Musical introuvable.'})

        if not artiste.style.is_connected(style):
            artiste.style.connect(style)

        return style

    def delete(self, style_uuid):
        """Déconnecte un style d’un artiste"""
        artiste = self.context.get('artiste')
        if not artiste:
            raise serializers.ValidationError("Artiste manquant dans le contexte.")

        try:
            style = StyleMusical.nodes.get(uuid=style_uuid)
        except StyleMusical.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Style Musical introuvable.'})

        artiste.style.disconnect(style)
        return style
