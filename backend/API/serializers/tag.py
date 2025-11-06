from django.urls import reverse
from rest_framework import serializers
from ..models import Tag
from ..errors import ValidatorUnique
from neomodel.exceptions import UniqueProperty


class TagSerializer(serializers.Serializer):
    """
    Sérializer du node Tag
    """
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def get_interviews(self, tag):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'tag_uuid': tag.uuid}))

    def get_extraits(self, tag):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'tag_uuid': tag.uuid}))

    def create(self, validated_data):
        """
        Création d'un tag
        """
        try:
            return Tag(**validated_data).save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)

    def update(self, tag, validated_data):
        """
        Modification d'un tag
        """
        for k, v in validated_data.items():
            setattr(tag, k, v)
        try:
            tag.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        return tag
