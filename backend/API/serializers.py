from rest_framework import serializers
from .models import Theme
from neomodel.exceptions import UniqueProperty

class ThemeSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        try:
            theme = Theme(**validated_data)
            theme.save()
            return theme
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Ce nom de thème existe déjà."}, 400)

    def update(self, instance: Theme, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Ce nom de thème existe déjà."}, 400)
        return instance
