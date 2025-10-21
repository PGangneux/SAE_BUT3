from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from neomodel.exceptions import DoesNotExist
from ..models import Artiste, Nationnalite


class ArtisteSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Input
    nationnalite_uuid = serializers.CharField(write_only=True, required=True)

    # Output
    styles_musicaux = serializers.SerializerMethodField(read_only=True)
    nationnalite = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)

    def get_styles_musicaux(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('style-musical-list', kwargs={'artiste_uuid': artiste.uuid}))}
    
    def get_nationnalite(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('nationnalite-detail', kwargs={'uuid': artiste.nationnalite.single().uuid}))}

    def get_interviews(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'artiste_uuid': artiste.uuid}))}

    def create(self, validated_data):
        nationnalite_uuid = validated_data.pop('nationnalite_uuid', None)
        artiste = Artiste(**validated_data).save()
        if nationnalite_uuid is not None:
            try: 
                artiste.pays.connect(Nationnalite.nodes.get(uuid=nationnalite_uuid))
            except DoesNotExist:
                raise NotFound('Nationnalite introuvable.', 404)
        return artiste

    def update(self, artiste, validated_data):
        for k, v in validated_data.items():
            setattr(artiste, k, v)
        return artiste.save()
