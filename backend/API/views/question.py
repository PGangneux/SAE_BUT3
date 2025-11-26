from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Question, Theme
from ..serializers import QuestionSerializer


class QuestionViewSet(BaseModelViewSet):
    """
    Renvoie les question
    """
    def __init__(self, **kwargs):
        super().__init__(QuestionSerializer, Question, 'texte', **kwargs)


class ThemeQuestionViewSet(SubBaseModelViewSet):
    """
    Renvoie les questions qui appartiennent à un thème
    """
    def __init__(self, **kwargs):
        super().__init__(QuestionSerializer, Question, 'theme_uuid', Theme, 'A_THEME', 'texte', **kwargs)