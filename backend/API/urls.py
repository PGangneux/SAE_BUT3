from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ExtraitViewSet, ThemeViewSet, QuestionViewSet, ThemeQuestionViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register(r'themes', ThemeViewSet, basename='theme')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'extraits', ExtraitViewSet, basename='extrait')

router_theme = NestedDefaultRouter(router, r'themes', lookup='theme')
router_theme.register(r'questions', ThemeQuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_theme.urls)),
]
