from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    ExtraitViewSet, InterviewViewSet,
    ThemeViewSet, QuestionViewSet,
    ThemeQuestionViewSet, InterviewExtraitViewSet,
    ArtisteViewSet, UtilisateurViewSet,
    ArtisteExtraitViewSet, QuestionExtraitViewSet,
    StyleMusicalViewSet, StyleMusicalArtisteViewSet,
    NationViewSet, InterviewsViewSet,
    NationArtisteViewSet, TagViewSet,
    TagInterviewViewSet, TagExtraitViewSet,
    InterviewTagViewSet, ExtraitTagViewSet,
    ArtisteStyleRelationShipViewSet,
    RecherchesArtistesViewSet, RegarderExtraitsViewSet,
    RegarderInterviewsViewSet, RecherchesQuestionsViewSet,
)

router = DefaultRouter()

router.register(r'themes', ThemeViewSet, basename='theme')
router_theme = NestedDefaultRouter(router, r'themes', lookup='theme')
router_theme.register(r'questions', ThemeQuestionViewSet, basename='question')

router.register(r'questions', QuestionViewSet, basename='question')
router_question = NestedDefaultRouter(router, r'questions', lookup='question')
router_question.register(r'extraits', QuestionExtraitViewSet, basename='extrait')

router.register(r'extraits', ExtraitViewSet, basename='extrait')
router_extrait = NestedDefaultRouter(router, r'extraits', lookup='extrait')
router_extrait.register(r'interviews', InterviewsViewSet, basename='interview')
router_extrait.register(r'tags', ExtraitTagViewSet, basename='tag')

router.register(r'interviews', InterviewViewSet, basename='interview')
router_interview = NestedDefaultRouter(router, r'interviews', lookup='interview')
router_interview.register(r'extraits', InterviewExtraitViewSet, basename='extrait')
router_interview.register(r'tags', InterviewTagViewSet, basename='tag')

router.register(r'artistes', ArtisteViewSet, basename='artiste')
router_artiste = NestedDefaultRouter(router, r'artistes', lookup='artiste')
router_artiste.register(r'extraits', ArtisteExtraitViewSet, basename='extrait')
router_artiste.register(r'styles', ArtisteStyleRelationShipViewSet, basename='style')

router.register(r'styles-musicaux', StyleMusicalViewSet, basename='style-musical')
router_style_musical = NestedDefaultRouter(router, r'styles-musicaux', lookup='stylemusical')
router_style_musical.register(r'artistes', StyleMusicalArtisteViewSet, basename='artiste')

router.register(r'nations', NationViewSet, basename='nation')
router_nation = NestedDefaultRouter(router, r'nations', lookup='nation')
router_nation.register(r'artistes', NationArtisteViewSet, basename='artiste')

router.register(r'tags', TagViewSet, basename='tag')
router_tag = NestedDefaultRouter(router, r'tags', lookup='tag')
router_tag.register(r'extraits', TagExtraitViewSet, basename='extrait')
router_tag.register(r'interviews', TagInterviewViewSet, basename='interview')

router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
router_utilisateur = NestedDefaultRouter(router, r'utilisateurs', lookup='utilisateur')
router_utilisateur.register(r'artistes', RecherchesArtistesViewSet, basename='artiste')
router_utilisateur.register(r'interviews', RegarderInterviewsViewSet, basename='interview')
router_utilisateur.register(r'extraits', RegarderExtraitsViewSet, basename='extrait')
router_utilisateur.register(r'questions', RecherchesQuestionsViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_theme.urls)),
    path('', include(router_question.urls)),
    path('', include(router_extrait.urls)),
    path('', include(router_interview.urls)),
    path('', include(router_artiste.urls)),
    path('', include(router_style_musical.urls)),
    path('', include(router_nation.urls)),
    path('', include(router_tag.urls)),
    path('', include(router_utilisateur.urls)),
]
