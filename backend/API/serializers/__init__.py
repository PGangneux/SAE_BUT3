import re
from datetime import datetime
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import serializers
from neomodel import StructuredNode, RelationshipTo, db
from neomodel.exceptions import UniqueProperty, DoesNotExist
from ..models import Tag, Utilisateur
from ..errors import ContextError, NotFound, ValidatorUnique


class Base(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)

    def __init__(self, Node: StructuredNode, *args, **kwargs):
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
            raise ValidatorUnique(
                re.search(
                    r"property\s+`(?P<prop>[^`]+)`\s*=",
                    str(error.message), re.IGNORECASE
                    ).group("prop")
                )
        return instance

    def update(self, instance, validated_data) -> StructuredNode:
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty as error:
            raise ValidatorUnique(
                re.search(
                    r"property\s+`(?P<prop>[^`]+)`\s*=",
                    str(error.message), re.IGNORECASE
                    ).group("prop")
                )
        return instance


class RelationShipBase(serializers.Serializer):
    uuid = serializers.CharField(required=True)

    def __init__(self, Node: StructuredNode, Context: StructuredNode, relationship: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Node = Node
        self.Context = Context
        self.relationship = relationship

    def get_url(self, url_name: str, kwargs:dict) -> str:
        request: HttpRequest = self.context.get('request')
        return request.build_absolute_uri(reverse(url_name, kwargs=kwargs))

    def create(self, validated_data):
        """
        Créer un lien entre deux éléments
        """
        context: StructuredNode = self.context.get(self.Context.__name__.lower())
        if not context:
            raise ContextError(self.Context)
        try:
            instance = self.Node.nodes.get(uuid=validated_data.pop('uuid', None))
        except DoesNotExist:
            raise NotFound(self.Node)
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
        context: StructuredNode = self.context.get(self.Context.__name__.lower())
        if not context:
            raise ContextError(self.Context)
        try:
            instance = self.Node.nodes.get(uuid=uuid)
        except DoesNotExist:
            raise NotFound(self.Node)
        relationship = getattr(context, self.relationship)
        relationship.disconnect(instance)
        return instance


class RelationShipUtilisateur(RelationShipBase):
    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)

    def __init__(self, Node: StructuredNode, relationship: str, *args, **kwargs):
        super().__init__(Node, Utilisateur, relationship, *args, **kwargs)

    def get_date_heure(self, instance):
        """
        Renvoie la date et l'heure :
        """
        utilisateur = self.context.get(self.Context.__name__.lower())
        if not utilisateur:
            raise ContextError(self.Context)
        query = "MATCH (i:"+ self.Node.__name__ + " {uuid:$uuid})<-[r:"+ self.relationship.upper() + "]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        res = db.cypher_query(query, {'uuid': instance.uuid, 'utilisateur': utilisateur.uuid})[0][0]
        return datetime.fromtimestamp(res[0].get('date_heure')).isoformat()
    

class RelationShipTag(RelationShipBase):
    name = serializers.CharField(read_only=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, Context: StructuredNode, relationship: str, *args, **kwargs):
        super().__init__(Tag, Context, relationship, *args, **kwargs)

    def get_interviews(self, tag):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url('interview-list', kwargs={'tag_uuid': tag.uuid})

    def get_extraits(self, tag):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url('extrait-list', kwargs={'tag_uuid': tag.uuid})



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

all = (
    ThemeSerializer,
    QuestionSerializer,
    ExtraitSerializer,
    InterviewSerializer,
    ArtisteSerializer,
    UtilisateurSerializer,
    StyleMusicalSerializer,
    NationSerializer,
    TagSerializer,
    StyleRelationShipSerializer,
    RecherchesArtistesSerializer,
    RegarderInterviewsSerializer,
    RegarderExtraitsSerializer,
    RecherchesQuestionsSerializer,
    InterviewsSerializer,
    PositionInputSerializer,
    TagsExtraitRelationShipSerializer,
    TagsInterviewRelationShipSerializer
)