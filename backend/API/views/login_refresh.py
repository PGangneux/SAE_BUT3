from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from neomodel import DoesNotExist, DeflateError
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Utilisateur


class LoginView(APIView):
    """
    Permet de récupérer un nouveau token d'accès
    Retourne le tokens JWT access
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh = request.data.get("refresh")

        a = RefreshToken(refresh)
        print(a)

        return JsonResponse(
            {
                "refresh": str(refresh),
                # "access": str(access),
                # "utilisateur": self.request.build_absolute_uri(
                #     reverse("utilisateur-detail", kwargs={"uuid": utilisateur.uuid})
                # ),
            },
            status=status.HTTP_200_OK,
        )
