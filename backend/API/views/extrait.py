from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode
from neo4j.exceptions import ServiceUnavailable
from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Artiste, Extrait, Interview, Question, Tag
from ..serializers import ExtraitSerializer
from ..errors import ConnexionDB, NotFound

class ExtraitViewSet(BaseModelViewSet):
    """
    Renvoie les extraits
    """
    def __init__(self, **kwargs):
        super().__init__(ExtraitSerializer, Extrait, 'titre', **kwargs)


class QuestionExtraitViewSet(SubBaseModelViewSet):
    """
    Renvoie les extraits qui répondent à la question
    """
    def __init__(self, **kwargs):
        super().__init__(ExtraitSerializer, Extrait, 'question_uuid', Question, 'POSE', 'titre', **kwargs)


class InterviewExtraitViewSet(SubBaseModelViewSet):
    """
    Renvoie les extraits qui appartiennent à une interview
    """
    def __init__(self, **kwargs):
        super().__init__(ExtraitSerializer, Extrait, 'interview_uuid', Interview, 'APPARTIENT_A', 'titre', 'r.position', **kwargs)
    
    def get_context_model(self) -> StructuredNode:
        """
        Récupère le node router
        """
        try:
            router_nodeset: NodeSet = self.router_model_class.nodes
            return router_nodeset.get(uuid=self.kwargs[self.router_lookup_field])
        # N'est jamais sensé passer pas ici, raise déjà dans get_nodeset
        except DoesNotExist: # pragma: no cover
            raise NotFound(self.router_model_class) # pragma: no cover
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable: # pragma: no cover
            raise ConnexionDB() # pragma: no cover

    def get_serializer_context(self):
        """
        Modification du contexte du sérializer
        """
        context = super().get_serializer_context()
        context_model_name: str = self.router_model_class.__name__
        context[context_model_name.lower()] = self.get_context_model()
        return context


class TagExtraitViewSet(SubBaseModelViewSet):
    """
    Renvoie les extraits en fonction d'un tag
    """
    def __init__(self, **kwargs):
        super().__init__(ExtraitSerializer, Extrait, 'tag_uuid', Tag, 'TAGS_EXTRAIT', 'titre', **kwargs)


class ArtisteExtraitViewSet(SubBaseModelViewSet):
    """
    Renvoie les extraits d'un artiste
    """
    def __init__(self, **kwargs):
        super().__init__(ExtraitSerializer, Extrait, 'artiste_uuid', Artiste, 'PARTICIPER', 'titre', **kwargs)
