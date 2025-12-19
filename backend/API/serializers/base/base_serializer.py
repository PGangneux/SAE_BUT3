import re
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import serializers
from neomodel import StructuredNode, RelationshipManager, NodeSet
from neomodel.exceptions import UniqueProperty, DeflateError, DoesNotExist, RequiredProperty
from ...errors import ValidatorUnique, ValidatorRequired, NotFound


class BaseSerializer(serializers.Serializer):
    """
    Classe de base contenant les méthodes pour la gestion des données (node)

    Raises:
        ValidatorUnique: Lors de la création et la mise à jour d'un node,
            vérifie que les propriétés uniques sont bien uniques
    """

    uuid = serializers.CharField(read_only=True)

    # Input:
    # {"uuid": {"relationship": "attribut relationship dans node", "node": Classe de node}, }
    input_fields = {}

    def __init__(self, node: StructuredNode, *args, **kwargs):
        """Création du Serializer pour un node du modèle

        Args:
            node (StructuredNode): Node du modèle
        """
        super().__init__(*args, **kwargs)
        self.node: StructuredNode = node

    def get_url(self, url_name: str, kwargs: dict) -> str:
        """Création d'une url absolue pour obtenir la ressource

        Args:
            url_name (str): nom de l'url dans le router
            kwargs (dict): données supplémentaires utiles à la création de l'url (uuid)

        Returns:
            str: url absolue pour obtenir la ressource
        """
        request: HttpRequest = self.context.get("request")
        return request.build_absolute_uri(reverse(url_name, kwargs=kwargs))

    def create(self, validated_data: dict) -> StructuredNode:
        """Création d'une instance de la classe du modèle (node)

        Args:
            validated_data (dict): Les données permettant de créer un node

        Raises:
            ValidatorUnique: Lors de la création et la mise à jour d'un node,
                vérifie que les propriétés uniques sont bien uniques

        Returns:
            StructuredNode: node nouvellement créer
        """
        instance: StructuredNode = self.node(**validated_data)
        try:
            instance.save()
        except UniqueProperty as error:
            raise ValidatorUnique(
                re.search(
                    r"property\s+`(?P<prop>[^`]+)`\s*=",
                    str(error.message),
                    re.IGNORECASE,
                ).group("prop")
            )
        except (DeflateError, RequiredProperty) as error:
            raise ValidatorRequired(error.property_name)

        for field in self.input_fields:
            uuid: str = validated_data.pop(field, None)
            if uuid:
                node_class: StructuredNode = self.input_fields[field]["node"]
                nodeset: NodeSet = node_class.nodes
                relationship: RelationshipManager = instance.__dict__.get(self.input_fields[field]["relationship"])
                try:
                    relationship.connect(nodeset.get(uuid=uuid))
                except DoesNotExist:
                    raise NotFound(node_class)
        return instance

    def update(self, instance: StructuredNode, validated_data: dict) -> StructuredNode:
        """Mise à jour d'une instance de la classe du modèle (node)

        Args:
            instance (StructuredNode): instance (node) à mettre à jour
            validated_data (dict): Les données permettant de créer un node

        Raises:
            ValidatorUnique: Lors de la création et la mise à jour d'un node,
                vérifie que les propriétés uniques sont bien uniques

        Returns:
            StructuredNode: node mise à jour
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty as error:
            raise ValidatorUnique(
                re.search(
                    r"property\s+`(?P<prop>[^`]+)`\s*=",
                    str(error.message),
                    re.IGNORECASE,
                ).group("prop")
            )
        except (DeflateError, RequiredProperty) as error:
            raise ValidatorRequired(error.property_name)

        for field in self.input_fields:
            uuid: str = validated_data.pop(field, None)
            if uuid:
                node_class: StructuredNode = self.input_fields[field]["node"]
                nodeset: NodeSet = node_class.nodes
                relationship: RelationshipManager = instance.__dict__.get(self.input_fields[field]["relationship"])
                try:
                    if relationship.single():
                        relationship.reconnect(
                            relationship.single(), nodeset.get(uuid=uuid)
                        )
                    else:
                        relationship.connect(nodeset.get(uuid=uuid))
                except DoesNotExist:
                    raise NotFound(node_class)
        return instance
