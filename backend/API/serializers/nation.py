from rest_framework import serializers
from ..serializers import BaseSerializer
from ..models import Nation


class NationSerializer(BaseSerializer):
    """
    Sérializer du node Nation
    """

    name = serializers.CharField(required=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Nation, *args, **kwargs)

    def get_artistes(self, nation):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.get_url("artiste-list", kwargs={"nation_uuid": nation.uuid})
