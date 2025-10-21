from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    ExtraitViewSet, InterviewViewSet,
    ThemeViewSet, QuestionViewSet,
    ThemeQuestionViewSet, InterviewExtraitViewSet,
    ArtisteViewSet, UtilisateurViewSet,
    ArtisteInterviewViewSet, QuestionExtraitViewSet,
    StyleMusicalViewSet, StyleMusicalArtisteViewSet,
    ArtisteStyleMusicalViewSet, NationnaliteViewSet,
)

router = DefaultRouter()
router.register(r'themes', ThemeViewSet, basename='theme')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'extraits', ExtraitViewSet, basename='extrait')
router.register(r'interviews', InterviewViewSet, basename='interview')
router.register(r'artistes', ArtisteViewSet, basename='artiste')
router.register(r'styles-musicaux', StyleMusicalViewSet, basename='style-musical')
router.register(r'nationnalites', NationnaliteViewSet, basename='nationnalite')
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

router_theme = NestedDefaultRouter(router, r'themes', lookup='theme')
router_theme.register(r'questions', ThemeQuestionViewSet, basename='question')

router_question = NestedDefaultRouter(router, r'questions', lookup='question')
router_question.register(r'extraits', QuestionExtraitViewSet, basename='extrait')

router_interview = NestedDefaultRouter(router, r'interviews', lookup='interview')
router_interview.register(r'extraits', InterviewExtraitViewSet, basename='extrait')

router_artiste = NestedDefaultRouter(router, r'artistes', lookup='artiste')
router_artiste.register(r'interviews', ArtisteInterviewViewSet, basename='interview')
router_artiste.register(r'styles-musicaux', ArtisteStyleMusicalViewSet, basename='style-musical')

routeur_style_musical = NestedDefaultRouter(router, r'styles-musicaux', lookup='stylemusical')
routeur_style_musical.register(r'artistes', StyleMusicalArtisteViewSet, basename='artiste')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_theme.urls)),
    path('', include(router_question.urls)),
    path('', include(router_interview.urls)),
    path('', include(router_artiste.urls)),
    path('', include(routeur_style_musical.urls)),
]
