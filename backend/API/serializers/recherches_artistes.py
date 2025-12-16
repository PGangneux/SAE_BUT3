from rest_framework import serializers
from ..serializers import RelationShipUtilisateurSerializer
from ..models import Artiste


class RecherchesArtistesSerializer(RelationShipUtilisateurSerializer):
    """
    Sérializer RelationShip recherches_artistes (Utilisateur <-> Artiste)
    """

    # Outputs
    name = serializers.CharField(read_only=True)
    info = serializers.CharField(read_only=True)
    nation = serializers.SerializerMethodField(read_only=True)
    styles = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Artiste, "recherches_artistes", *args, **kwargs)

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
        return self.get_url("extrait-list", kwargs={"artiste_uuid": artiste.uuid})
