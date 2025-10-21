from django.urls import reverse
from rest_framework import serializers
from ..models import Nationnalite


class NationnaliteSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def get_artistes(self, nationnalite):
        return {"url": self.context.get('request').build_absolute_uri(reverse('artiste-list', kwargs={'nationnalite_uuid': nationnalite.uuid}))}

    def create(self, validated_data):
        return Nationnalite(**validated_data).save()

    def update(self, nationnalite, validated_data):
        for k, v in validated_data.items():
            setattr(nationnalite, k, v)
        return nationnalite.save()
