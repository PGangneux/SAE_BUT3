from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from neomodel import DoesNotExist, NodeSet

from ...models import Utilisateur


class TokenObtain(TokenObtainPairSerializer):
    """
    Permet de se connecter avec pseudo ou email + mot de passe.
    Retourne les tokens JWT (access, refresh) et lien utilisateur
    """

    def validate(self, attrs):
        request: HttpRequest = self.context.get("request")

        username = attrs.get("username")
        password = attrs.get("password")

        print(username, password)

        utilisateur: Utilisateur
        utilisateur_nodeset : NodeSet = Utilisateur.nodes
        # Recherche par email ou pseudo
        # Test dans cette ordre à cause d'un défaut inérant à RegexProperty
        try:
            utilisateur = utilisateur_nodeset.get(pseudo=username)
        except DoesNotExist:
            try:
                utilisateur = utilisateur_nodeset.get(email=username)
            except:
                raise AuthenticationFailed("Identifiants invalides")

        # Vérification du mot de passe
        stored_password = utilisateur.password
        valid = check_password(password, stored_password) or password == stored_password
        if not valid:
            raise AuthenticationFailed("Identifiants invalides")

        refresh: RefreshToken = self.get_token(utilisateur)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "utilisateur": request.build_absolute_uri(
                reverse("utilisateur-detail", kwargs={"uuid": utilisateur.uuid})
            ),
        }
