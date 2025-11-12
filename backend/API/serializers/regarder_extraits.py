from rest_framework import serializers
from ..serializers import RelationShipUtilisateur
from ..models import Extrait


class RegarderExtraitsSerializer(RelationShipUtilisateur):
    """
    Sérializer RelationShip regarder_extraits (Utilisateur <-> Extrait)
    """

    # Outputs
    titre = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    youtube_url = serializers.CharField(read_only=True)
    vimeo_url = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateField(read_only=True)
    duree = serializers.IntegerField(read_only=True)
    artiste = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Extrait, 'regarder_extraits', *args, **kwargs)

    def get_artiste(self, extrait):
        """
        Renvoie un lien propre vers l'artiste :
        """
        artiste = extrait.interviewer.single()
        return self.get_url('artiste-detail', kwargs={'uuid': artiste.uuid}) if artiste else None

    def get_question(self, extrait):
        """
        Renvoie un lien propre vers la question :
        """
        question = extrait.question.single()
        return self.get_url('question-detail', kwargs={'uuid': question.uuid}) if question else None

    def get_interviews(self, extrait):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url('interview-list', kwargs={'extrait_uuid': extrait.uuid})

    def get_tags(self, extrait):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url('tag-list', kwargs={'extrait_uuid': extrait.uuid})
