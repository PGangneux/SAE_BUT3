from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import DoesNotExist, UniqueProperty
from ..errors import ValidatorUnique, NotFound
from ..models import Artiste, Nation


class ArtisteSerializer(serializers.Serializer):
    """
    Sérializer du node Artiste
    """
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Input
    nation_uuid = serializers.CharField(write_only=True, required=False,)

    # Output
    nation = serializers.SerializerMethodField(read_only=True)
    styles = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def get_nation(self, artiste):
        """
        Renvoie un lien propre vers la nation :
        """
        nation = artiste.nationalite.single()
        return self.context.get('request').build_absolute_uri(reverse('nation-detail', kwargs={'uuid': nation.uuid})) if nation else None 

    def get_styles(self, artiste):
        """
        Renvoie un lien propre vers les styles :
        """
        return self.context.get('request').build_absolute_uri(reverse('style-list', kwargs={'artiste_uuid': artiste.uuid}))

    def get_extraits(self, artiste):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'artiste_uuid': artiste.uuid}))

    def create(self, validated_data):
        """
        Création d'un artiste
        """
        nation_uuid = validated_data.pop('nation_uuid', None)
        artiste = Artiste(**validated_data)
        try:
            artiste.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        if nation_uuid is not None:
            try: 
                artiste.nationalite.connect(Nation.nodes.get(uuid=nation_uuid))
            except DoesNotExist:
                raise NotFound(Nation)
        return artiste

    def update(self, artiste, validated_data):
        """
        Modification d'un artiste
        """
        nation_uuid = validated_data.pop('nation_uuid', None)
        for k, v in validated_data.items():
            setattr(artiste, k, v)
        try:
            artiste.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        if nation_uuid is not None:
            try:
                if artiste.nationalite:
                    artiste.nationalite.disconnect(artiste.nationalite.single())
                artiste.nationalite.connect(Nation.nodes.get(uuid=nation_uuid))
            except DoesNotExist:
                raise NotFound(Nation)
        return artiste.save()
