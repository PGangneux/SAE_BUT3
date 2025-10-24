from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import UniqueProperty
from ..models import Question, Theme


class QuestionSerializer(serializers.Serializer):
    """
    Sérializer du node Question
    """
    uuid = serializers.CharField(read_only=True)
    texte = serializers.CharField(required=True)

    # Inputs
    theme_uuid = serializers.CharField(write_only=True, required=False)

    # Outputs
    theme = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def get_theme(self, question):
        """
        Renvoie un lien propre vers le theme :
        """
        theme = question.theme.single()
        return {"url": self.context.get('request').build_absolute_uri(reverse('theme-detail', kwargs={'uuid': theme.uuid}))} if theme else None

    def get_extraits(self, question):
        """
        Renvoie un lien propre vers les extraits :
        """
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'question_uuid': question.uuid}))}

    def create(self, validated_data):
        """
        Création d'une question
        """
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
        """
        Modification d'une question
        """
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
