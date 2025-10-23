from datetime import datetime
from django.urls import reverse
from rest_framework import serializers
from neomodel import db
from ..models import Question


class RecherchesQuestionsSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True)

    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)
    texte = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    theme = serializers.SerializerMethodField(read_only=True)

    def get_date_heure(self, question):
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")
        query = "MATCH (i:Question {uuid:$artiste})<-[r:RECHERCHES_QUESTIONS]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        res = db.cypher_query(query, {'question': question.uuid, 'utilisateur': utilisateur.uuid})[0][0]
        return datetime.fromtimestamp(res[0].get('date_heure')).isoformat()

    def get_extraits(self, question):
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'question_uuid': question.uuid}))}

    def get_theme(self, question):
        """
        Renvoie un lien vers le thème
        """
        if question.theme:
            return {"url": self.context.get('request').build_absolute_uri(reverse('theme-detail', kwargs={'uuid': question.theme.single().uuid}))}
        return None

    def create(self, validated_data):
        """Connecte une question à un utilisateur"""
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")

        question_uuid = validated_data['uuid']
        try:
            question = Question.nodes.get(uuid=question_uuid)
        except Question.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Question introuvable.'})

        if not utilisateur.recherches_questions.is_connected(question):
            utilisateur.recherches_questions.connect(question)

        return question

    def delete(self, question_uuid):
        """Déconnecte une question d’un utilisateur"""
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")

        try:
            question = Question.nodes.get(uuid=question_uuid)
        except Question.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Question introuvable.'})

        utilisateur.recherches_questions.disconnect(question)
        return question
