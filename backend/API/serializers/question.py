from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import UniqueProperty
from ..models import Question, Theme


class QuestionSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    texte = serializers.CharField(required=True)

    # Inputs
    theme_uuid = serializers.CharField(write_only=True, required=False)

    # Outputs
    extraits = serializers.SerializerMethodField(read_only=True)
    theme = serializers.SerializerMethodField(read_only=True)

    def get_extraits(self, question):
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'question_uuid': question.uuid}))}

    def get_theme(self, question):
        """
        Renvoie un lien propre vers le thème
        """
        if question.theme:
            return {"url": self.context.get('request').build_absolute_uri(reverse('theme-detail', kwargs={'uuid': question.theme.single().uuid}))}
        return None

    def create(self, validated_data):
        theme_uuid = validated_data.pop("theme_uuid", None)
        try:
            question = Question(**validated_data).save()
        except UniqueProperty:
            raise serializers.ValidationError({"text": "Cette question existe déjà"}, 400)
        if theme_uuid:
            try:
                theme = Theme.nodes.get(uuid=theme_uuid)
                question.theme.connect(theme)
            except Theme.DoesNotExist:
                raise serializers.ValidationError({"theme_uuid": "Thème introuvable."}, 404)
        return question

    def update(self, instance, validated_data):
        theme_uuid = validated_data.pop("theme_uuid", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Cette question existe déjà."}, 400)
        try:
            instance.theme.disconnect(instance.theme.single())
            if theme_uuid:
                instance.theme.connect(Theme.nodes.get(uuid=theme_uuid))
        except Theme.DoesNotExist:
            raise serializers.ValidationError({"theme_uuid": "Thème introuvable."}, 404)
        return instance
