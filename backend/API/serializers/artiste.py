from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from ..errors import NotFound
from ..models import Artiste, Nation
from ..serializers import BaseSerializer


class ArtisteSerializer(BaseSerializer):
    """
    Sérializer du node Artiste
    """

    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Input
    nation_uuid = serializers.CharField(
        write_only=True,
        required=False,
    )

    # Output
    nation = serializers.SerializerMethodField(read_only=True)
    styles = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Artiste, *args, **kwargs)

    def get_nation(self, artiste):
        """
        Renvoie un lien propre vers la nation :
        """
        nation = artiste.nationalite.single()
        return (
            self.get_url("nation-detail", kwargs={"uuid": nation.uuid})
            if nation
            else None
        )

    def get_styles(self, artiste):
        """
        Renvoie un lien propre vers les styles :
        """
        return self.get_url("style-list", kwargs={"artiste_uuid": artiste.uuid})

    def get_extraits(self, artiste):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", {"artiste_uuid": artiste.uuid})

    def create(self, validated_data):
        """
        Création d'un artiste
        """
        nation_uuid = validated_data.pop("nation_uuid", None)
        artiste = super().create(validated_data)
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
        nation_uuid = validated_data.pop("nation_uuid", None)
        artiste = super().update(artiste, validated_data)
        if nation_uuid is not None:
            try:
                if artiste.nationalite:
                    artiste.nationalite.disconnect(artiste.nationalite.single())
                artiste.nationalite.connect(Nation.nodes.get(uuid=nation_uuid))
            except DoesNotExist:
                raise NotFound(Nation)
        return artiste.save()
