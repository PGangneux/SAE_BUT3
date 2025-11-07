from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import serializers
from ..models import Utilisateur
from ..errors import ValidatorUnique
from neomodel.exceptions import UniqueProperty


class UtilisateurSerializer(serializers.Serializer):
    """
    Sérializer du node Utilisateur
    """
    uuid = serializers.CharField(read_only=True)
    pseudo = serializers.CharField(required=True)
    prenom = serializers.CharField(required=True)
    nom = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    is_admin = serializers.BooleanField()

    # Outputs
    recherches_artistes = serializers.SerializerMethodField(read_only=True)
    regarder_interviews = serializers.SerializerMethodField(read_only=True)
    regarder_extraits = serializers.SerializerMethodField(read_only=True)
    recherches_questions = serializers.SerializerMethodField(read_only=True)

    def get_recherches_artistes(self, utilisateur):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.context.get('request').build_absolute_uri(reverse('artiste-list', kwargs={'utilisateur_uuid': utilisateur.uuid}))

    def get_regarder_interviews(self, utilisateur):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'utilisateur_uuid': utilisateur.uuid}))

    def get_regarder_extraits(self, utilisateur):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'utilisateur_uuid': utilisateur.uuid}))

    def get_recherches_questions(self, utilisateur):
        """
        Renvoie un lien propre vers les questions :
        """
        return self.context.get('request').build_absolute_uri(reverse('question-list', kwargs={'utilisateur_uuid': utilisateur.uuid}))

    def create(self, validated_data):
        """
        Création d'un utilisateur
        """
        # hash password
        validated_data['password'] = make_password(validated_data.pop('password'))
        try:
            return Utilisateur(**validated_data).save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)


    def update(self, utilisateur, validated_data):
        """
        Modification d'un utilisateur
        """
        # hash password
        pwd = validated_data.pop('password', None)
        if pwd:
            utilisateur.password = make_password(pwd)
        for k, v in validated_data.items():
            setattr(utilisateur, k, v)
        try:
            return utilisateur.save()
        except UniqueProperty as error:
            raise ValidatorUnique(error.message)
