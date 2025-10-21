from django.urls import reverse
from rest_framework import serializers
from ..models import Nation


class NationSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def get_artistes(self, nation):
        return {"url": self.context.get('request').build_absolute_uri(reverse('artiste-list', kwargs={'nation_uuid': nation.uuid}))}

    def create(self, validated_data):
        return Nation(**validated_data).save()

    def update(self, nation, validated_data):
        for k, v in validated_data.items():
            setattr(nation, k, v)
        return nation.save()
