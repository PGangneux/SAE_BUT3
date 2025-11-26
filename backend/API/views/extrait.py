from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Artiste, Extrait, Interview, Question, Tag
from ..serializers import ExtraitSerializer


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
