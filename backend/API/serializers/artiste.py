from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from neomodel.exceptions import DoesNotExist
from ..models import Artiste, Nation


class ArtisteSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Input
    nation_uuid = serializers.CharField(write_only=True, required=False,)

    # Output
    styles = serializers.SerializerMethodField(read_only=True)
    nation = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)

    def get_styles(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('style-list', kwargs={'artiste_uuid': artiste.uuid}))}
    
    def get_nation(self, artiste):
        if artiste.nationalite:
            return {"url": self.context.get('request').build_absolute_uri(reverse('nation-detail', kwargs={'uuid': artiste.nationalite.single().uuid}))}
        return None

    def get_interviews(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'artiste_uuid': artiste.uuid}))}

    def create(self, validated_data):
        nation_uuid = validated_data.pop('nation_uuid', None)
        artiste = Artiste(**validated_data).save()
        if nation_uuid is not None:
            try: 
                artiste.nationalite.connect(Nation.nodes.get(uuid=nation_uuid))
            except DoesNotExist:
                raise NotFound('Nation introuvable.', 404)
        return artiste

    def update(self, artiste, validated_data):
        nation_uuid = validated_data.pop('nation_uuid', None)
        for k, v in validated_data.items():
            setattr(artiste, k, v)
        if nation_uuid is not None:
            try:
                if artiste.nationalite:
                    artiste.nationalite.disconnect(artiste.nationnalite.single())
                artiste.nationalite.connect(Nation.nodes.get(uuid=nation_uuid))
            except DoesNotExist:
                raise NotFound('Nation introuvable.', 404)
        return artiste.save()
