from django.urls import reverse
from rest_framework import serializers
from ..models import Artiste


class ArtisteSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Output
    interviews = serializers.SerializerMethodField(read_only=True)

    def get_interviews(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'artiste_uuid': artiste.uuid}))}

    def create(self, validated_data):
        return Artiste(**validated_data).save()

    def update(self, artiste, validated_data):
        for k, v in validated_data.items():
            setattr(artiste, k, v)
        return artiste.save()
