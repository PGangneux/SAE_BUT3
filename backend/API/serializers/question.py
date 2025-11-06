from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import UniqueProperty, DoesNotExist
from ..models import Question, Theme
from ..errors import ValidatorUnique, NotFound


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
        return self.context.get('request').build_absolute_uri(reverse('theme-detail', kwargs={'uuid': theme.uuid})) if theme else None

    def get_extraits(self, question):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'question_uuid': question.uuid}))

    def create(self, validated_data):
        """
        Création d'une question
        """
        theme_uuid = validated_data.pop("theme_uuid", None)
        question = Question(**validated_data)
        try:
            question.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        if theme_uuid:
            try:
                theme = Theme.nodes.get(uuid=theme_uuid)
                question.theme.connect(theme)
            except DoesNotExist:
                raise NotFound(Theme)
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
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        try:
            theme = instance.theme.single()
            if theme:
                instance.theme.disconnect(theme)
            if theme_uuid:
                instance.theme.connect(Theme.nodes.get(uuid=theme_uuid))
        except DoesNotExist:
                raise NotFound(Theme)
        return instance
