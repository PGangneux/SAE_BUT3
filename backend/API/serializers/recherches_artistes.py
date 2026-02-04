from rest_framework import serializers
from ..serializers import RelationShipUtilisateurSerializer
from ..models import Artiste


class RecherchesArtistesSerializer(RelationShipUtilisateurSerializer):
    """
    Sérializer RelationShip recherches_artistes (Utilisateur <-> Artiste)
    """

    # Outputs
    name = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Artiste, "recherches_artistes", *args, **kwargs)

    def get_extraits(self, artiste):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"artiste_uuid": artiste.uuid})
