from .base import BaseModelViewSet, SubBaseModelViewSet, BaseRelationShipViewSet
from .theme import ThemeViewSet
from .question import QuestionViewSet, ThemeQuestionViewSet
from .extrait import (
    ExtraitViewSet,
    TagExtraitViewSet,
    ArtisteExtraitViewSet,
    QuestionExtraitViewSet,
    InterviewExtraitViewSet,
)
from .interview import InterviewViewSet, TagInterviewViewSet
from .artiste import ArtisteViewSet, NationArtisteViewSet, StyleMusicalArtisteViewSet
from .utilisateur import UtilisateurViewSet
from .style_musical import StyleMusicalViewSet
from .nation import NationViewSet
from .tag import TagViewSet
from .style import ArtisteStyleRelationShipViewSet
from .recherches_artistes import RecherchesArtistesViewSet
from .regarder_interviews import RegarderInterviewsViewSet
from .regarder_extraits import RegarderExtraitsViewSet
from .recherches_questions import RecherchesQuestionsViewSet
from .interviews import InterviewsViewSet
from .tags_extrait import TagsExtraitRelationShipViewSet
from .tags_interview import TagsInterviewRelationShipViewSet
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
    "NationArtisteViewSet",
    "StyleMusicalArtisteViewSet",
    "UtilisateurViewSet",
    "StyleMusicalViewSet",
    "NationViewSet",
    "TagViewSet",
    "ArtisteStyleRelationShipViewSet",
    "RecherchesArtistesViewSet",
    "RegarderInterviewsViewSet",
    "RegarderExtraitsViewSet",
    "RecherchesQuestionsViewSet",
    "InterviewsViewSet",
    "TagsExtraitRelationShipViewSet",
    "TagsInterviewRelationShipViewSet",
    "LoginView",
    "Recommandation",
)
