from neomodel import StructuredNode
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import serializers
from neomodel.exceptions import UniqueProperty
from ..errors import ValidatorUnique

class Base(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)

    def __init__(self, Node: StructuredNode, *args, **kwargs):
        """
        Compatible DRF : accepte *args / **kwargs tels que DRF les fournit.
        Node (la classe StructuredNode) est passée en kwarg optionnel.
        """
        super().__init__(*args, **kwargs)
        self.Node = Node

    def get_url(self, url_name: str, kwargs:dict) -> str:
        request: HttpRequest = self.context.get('request')
        return request.build_absolute_uri(reverse(url_name, kwargs=kwargs))

    def create(self, validated_data) -> StructuredNode:
        instance = self.Node(**validated_data)
        try:
            instance.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        return instance

    def update(self, instance, validated_data) -> StructuredNode:
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
        return instance


from .theme import ThemeSerializer
from .question import QuestionSerializer
from .extrait import ExtraitSerializer
from .interview import InterviewSerializer
from .artiste import ArtisteSerializer
from .utilisateur import UtilisateurSerializer
from .style_musical import StyleMusicalSerializer
from .nation import NationSerializer
from .tag import TagSerializer
from .style import StyleRelationShipSerializer
from .recherches_artistes import RecherchesArtistesSerializer
from .regarder_interviews import RegarderInterviewsSerializer
from .regarder_extraits import RegarderExtraitsSerializer
from .recherches_questions import RecherchesQuestionsSerializer
from .interviews import InterviewsSerializer, PositionInputSerializer
from .tags_extrait import TagsExtraitRelationShipSerializer
from .tags_interview import TagsInterviewRelationShipSerializer
