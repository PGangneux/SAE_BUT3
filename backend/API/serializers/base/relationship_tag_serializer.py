from rest_framework import serializers
from neomodel import StructuredNode
from ...models import Tag
from ..base import BaseRelationShipSerializer


class RelationShipTagSerializer(BaseRelationShipSerializer):
    name = serializers.CharField(read_only=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(
        self, context_node: StructuredNode, relationship: str, *args, **kwargs
    ):
        super().__init__(Tag, context_node, relationship, *args, **kwargs)

    def get_interviews(self, tag):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url("interview-list", kwargs={"tag_uuid": tag.uuid})

    def get_extraits(self, tag):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"tag_uuid": tag.uuid})
