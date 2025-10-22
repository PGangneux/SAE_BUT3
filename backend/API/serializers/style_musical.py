from django.urls import reverse
from rest_framework import serializers
from ..models import StyleMusical


class StyleMusicalSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def get_artistes(self, style_musical):
        return {"url": self.context.get('request').build_absolute_uri(reverse('artiste-list', kwargs={'stylemusical_uuid': style_musical.uuid}))}

    def create(self, validated_data):
        return StyleMusical(**validated_data).save()

    def update(self, style_musical, validated_data):
        for k, v in validated_data.items():
            setattr(style_musical, k, v)
        return style_musical.save()
