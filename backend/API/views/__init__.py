from .base import BaseModelViewSet, SubBaseModelViewSet, BaseRelationShipViewSet
from .theme import ThemeViewSet
from .question import QuestionViewSet, ThemeQuestionViewSet
from .extrait import (
    ExtraitViewSet,
    TagExtraitViewSet,
    ArtisteExtraitViewSet,
    QuestionExtraitViewSet,
    InterviewExtraitViewSet,
    AudioExtraitViewSet,
)
from .interview import InterviewViewSet, TagInterviewViewSet
from .artiste import ArtisteViewSet
from .utilisateur import UtilisateurViewSet
from .tag import TagViewSet
from .recherches_artistes import RecherchesArtistesViewSet
from .regarder_interviews import RegarderInterviewsViewSet
from .regarder_extraits import RegarderExtraitsViewSet
from .recherches_questions import RecherchesQuestionsViewSet
from .interviews import InterviewsViewSet
from .tags_extrait import TagsExtraitRelationShipViewSet
from .tags_interview import TagsInterviewRelationShipViewSet
from .audio import AudioViewSet
from .audios import AudiosViewSet
from .login import LoginView
from .recommandation import Recommandation


__all__ = (
    "BaseModelViewSet",
    "SubBaseModelViewSet",
    "BaseRelationShipViewSet",
    "ThemeViewSet",
    "QuestionViewSet",
    "ThemeQuestionViewSet",
    "ExtraitViewSet",
    "TagExtraitViewSet",
    "ArtisteExtraitViewSet",
    "QuestionExtraitViewSet",
    "InterviewExtraitViewSet",
    "InterviewViewSet",
    "TagInterviewViewSet",
    "ArtisteViewSet",
    "UtilisateurViewSet",
    "TagViewSet",
    "RecherchesArtistesViewSet",
    "RegarderInterviewsViewSet",
    "RegarderExtraitsViewSet",
    "RecherchesQuestionsViewSet",
    "InterviewsViewSet",
    "TagsExtraitRelationShipViewSet",
    "TagsInterviewRelationShipViewSet",
    "AudioViewSet",
    "AudiosViewSet",
    "AudioExtraitViewSet",
    "LoginView",
    "Recommandation",
)
