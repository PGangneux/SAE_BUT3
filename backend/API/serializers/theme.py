from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import UniqueProperty
from ..models import Theme


class ThemeSerializer(serializers.Serializer):
    """
    Sérializer du node Theme
    """
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Outputs
    questions = serializers.SerializerMethodField(read_only=True)

    def get_questions(self, theme):
        """
        Renvoie un lien propre vers les questions :
        """
        return {"url": self.context.get('request').build_absolute_uri(reverse('question-list', kwargs={'theme_uuid': theme.uuid}))}

    def create(self, validated_data):
        """
        Création d'un theme
        """
        try:
            return Theme(**validated_data).save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Ce nom de thème existe déjà."}, 400)

    def update(self, instance: Theme, validated_data):
        """
        Modification d'un theme
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Ce nom de thème existe déjà."}, 400)
        return instance
