from django.urls import reverse
from django.http import HttpRequest
from rest_framework import serializers
from neomodel import StructuredNode, RelationshipTo
from neomodel.exceptions import DoesNotExist
from ...errors import ContextError, NotFound


class BaseRelationShipSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True)

    def __init__(
        self,
        node: StructuredNode,
        context_node: StructuredNode,
        relationship: str,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.node = node
        self.context_node = context_node
        self.relationship = relationship

    def get_url(self, url_name: str, kwargs: dict) -> str:
        request: HttpRequest = self.context.get("request")
        return request.build_absolute_uri(reverse(url_name, kwargs=kwargs))

    def create(self, validated_data):
        """
        Créer un lien entre deux éléments
        """
        context: StructuredNode = self.context.get(self.context_node.__name__.lower())
        if not context:
            raise ContextError(self.context_node)
        try:
            instance = self.node.nodes.get(uuid=validated_data.pop("uuid", None))
        except DoesNotExist:
            raise NotFound(self.node)
        relationship: RelationshipTo = getattr(context, self.relationship)
        if not relationship.is_connected(instance):
            if validated_data:
                relationship.connect(instance, validated_data)
            else:
                relationship.connect(instance)
        return instance

    def delete(self, uuid):
        """
        Supprime un lien entre deux éléments
        """
        context: StructuredNode = self.context.get(self.context_node.__name__.lower())
        if not context:
            raise ContextError(self.context_node)
        try:
            instance = self.node.nodes.get(uuid=uuid)
        except DoesNotExist:
            raise NotFound(self.node)
        relationship = getattr(context, self.relationship)
        relationship.disconnect(instance)
        return instance
