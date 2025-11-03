from django.urls import reverse
from rest_framework import serializers
from ..models import StyleMusical

class StyleRelationShipSerializer(serializers.Serializer):
    """
    Sérializer RelationShip style (Artiste <-> Style)
    """
    uuid = serializers.CharField(required=True)
    name = serializers.CharField(read_only=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def get_artistes(self, style_musical):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.context.get('request').build_absolute_uri(reverse('artiste-list', kwargs={'stylemusical_uuid': style_musical.uuid}))

    def create(self, validated_data):
        """
        Connecte un style musical à un artiste
        """
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
        """
        Déconnecte un style musical d’un artiste
        """
        artiste = self.context.get('artiste')
        if not artiste:
            raise serializers.ValidationError("Artiste manquant dans le contexte.")

        try:
            style = StyleMusical.nodes.get(uuid=style_uuid)
        except StyleMusical.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Style Musical introuvable.'})

        artiste.style.disconnect(style)
        return style
