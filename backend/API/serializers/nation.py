from django.urls import reverse
from rest_framework import serializers
from ..models import Nation


class NationSerializer(serializers.Serializer):
    """
    Sérializer du node Nation
    """
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def get_artistes(self, nation):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.context.get('request').build_absolute_uri(reverse('artiste-list', kwargs={'nation_uuid': nation.uuid}))

    def create(self, validated_data):
        """
        Création d'une nation
        """
        return Nation(**validated_data).save()

    def update(self, nation, validated_data):
        """
        Modification d'une nation
        """
        for k, v in validated_data.items():
            setattr(nation, k, v)
        return nation.save()
