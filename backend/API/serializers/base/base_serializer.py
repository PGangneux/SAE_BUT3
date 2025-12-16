import re
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import serializers
from neomodel import StructuredNode
from neomodel.exceptions import UniqueProperty
from ...errors import ValidatorUnique


class BaseSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)

    def __init__(self, node: StructuredNode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node: StructuredNode = node

    def get_url(self, url_name: str, kwargs: dict) -> str:
        request: HttpRequest = self.context.get("request")
        return request.build_absolute_uri(reverse(url_name, kwargs=kwargs))

    def create(self, validated_data: dict) -> StructuredNode:
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
        return instance

    def update(self, instance: StructuredNode, validated_data: dict) -> StructuredNode:
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
        return instance
