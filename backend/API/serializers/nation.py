from rest_framework import serializers
from ..models import Nation


class NationSerializer(serializers.Serializer):
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
        return self.get_url('artiste-list', kwargs={'nation_uuid': nation.uuid})

    def create(self, validated_data):
        """
        Création d'une nation
        """
        return super().create(validated_data)

    def update(self, nation, validated_data):
        """
        Modification d'une nation
        """
        return super().update(nation, validated_data)
