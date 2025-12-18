from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from ..errors import NotFound
from ..models import Artiste
from ..serializers import BaseSerializer


class ArtisteSerializer(BaseSerializer):
    """
    Sérializer du node Artiste
    """

    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)


    # Output
    styles = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Artiste, *args, **kwargs)


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

