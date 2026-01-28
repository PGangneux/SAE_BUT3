from rest_framework import serializers
from neomodel import db
from ..serializers import BaseSerializer
from ..models import Artiste, Audio, Extrait, Question


class ExtraitSerializer(BaseSerializer):
    """
    Sérializer du node Extrait
    """

    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    youtube_url = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateField(required=False, allow_null=True)
    duree = serializers.IntegerField(required=True)

    # Input:
    input_fields = {
        "artiste_uuid": {"relationship": "interviewer", "node": Artiste},
        "question_uuid": {"relationship": "question", "node": Question},
        "audio_uuid": {"relationship": "audios", "node": Audio},
    }
    artiste_uuid = serializers.CharField(write_only=True, required=False)
    question_uuid = serializers.CharField(write_only=True, required=False)
    audio_uuid = serializers.CharField(write_only=True, required=False)

    # Output:
    artiste = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    audios = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    position = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """Retire le champ `position` si aucune interview n'est dans le contexte."""
        super().__init__(Extrait, *args, **kwargs)
        if not self.context.get("interview"):
            self.fields.pop("position", None)

    def get_artiste(self, extrait):
        """
        Renvoie un lien propre vers l'artiste :
        """
        artiste = extrait.interviewer.single()
        return (
            self.get_url("artiste-detail", kwargs={"uuid": artiste.uuid})
            if artiste
            else None
        )

    def get_question(self, extrait):
        """
        Renvoie un lien propre vers la question :
        """
        question = extrait.question.single()
        return (
            self.get_url("question-detail", kwargs={"uuid": question.uuid})
            if question
            else None
        )

    def get_interviews(self, extrait):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url("interview-list", kwargs={"extrait_uuid": extrait.uuid})

    def get_audios(self, extrait: Extrait):
        """Renvoie un lien vers les audios

        Args:
            extrait (Extrait): un extrait
        """
        return self.get_url("audio-list", kwargs={"extrait_uuid": extrait.uuid})

    def get_tags(self, extrait):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url("tag-list", kwargs={"extrait_uuid": extrait.uuid})

    def get_position(self, extrait):
        interview = self.context.get("interview")
        return int(
            db.cypher_query(
                "MATCH (e:Extrait {uuid:$extrait_uuid})-[r:APPARTIENT_A]->(i:Interview {uuid:$interview_uuid}) RETURN r.position AS pos",
                {"extrait_uuid": extrait.uuid, "interview_uuid": interview.uuid},
            )[0][0][0]
        )
