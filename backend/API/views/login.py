from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from neomodel import DoesNotExist
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Utilisateur


class LoginView(APIView):
    """
    Permet de se connecter avec pseudo ou email + mot de passe.
    Retourne les tokens JWT (access, refresh)
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        identifiant = request.data.get("identifiant")
        password = request.data.get("password")

        if not identifiant or not password:
            return Response(
                {"detail": "Veuillez fournir identifiant et mot de passe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Recherche par email ou pseudo
        try:
            utilisateur = Utilisateur.nodes.get(email=identifiant)
        except DoesNotExist:
            try:
                utilisateur = Utilisateur.nodes.get(pseudo=identifiant)
            except DoesNotExist:
                return Response(
                    {"detail": "Identifiants invalides."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        # Vérification du mot de passe
        stored_password = utilisateur.password
        valid = check_password(password, stored_password) or password == stored_password
        if not valid:
            return Response(
                {"detail": "Identifiants invalides."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Génération des tokens avec SimpleJWT
        refresh = RefreshToken.for_user(utilisateur)
        access = refresh.access_token

        return JsonResponse(
            {
                "refresh": str(refresh),
                "access": str(access),
                "utilisateur": self.request.build_absolute_uri(
                    reverse("utilisateur-detail", kwargs={"uuid": utilisateur.uuid})
                ),
            },
            status=status.HTTP_200_OK,
        )
