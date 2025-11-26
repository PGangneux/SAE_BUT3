from rest_framework import serializers
from ..serializers import Base
from ..models import Interview


class InterviewSerializer(Base):
    """
    Sérializer du node Interview
    """
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    occasion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Outputs
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Interview, *args, **kwargs)

    def get_extraits(self, interview):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url('extrait-list', kwargs={'interview_uuid': interview.uuid})

    def get_tags(self, interview):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url('tag-list', kwargs={'interview_uuid': interview.uuid})
