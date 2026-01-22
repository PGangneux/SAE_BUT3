from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from rest_framework.exceptions import NotAuthenticated
from neo4j.exceptions import ServiceUnavailable
from .models import Utilisateur
from .errors import ConnexionDB


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Utilisateur

class Neo4jJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed("Token invalide")

        try:
            return Utilisateur.nodes.get(uuid=user_id)
        except Utilisateur.DoesNotExist:
            raise AuthenticationFailed("Utilisateur introuvable")



def get_current_user(request):
    authorization = request.headers.get("Authorization", None)
    if authorization:
        token = authorization.split()[1]
        try:
            access = AccessToken(token)
        except ExpiredTokenError:
            raise NotAuthenticated()
        try:
            user: Utilisateur = Utilisateur.nodes.get(uuid=access["user_id"])
        except ServiceUnavailable:
            raise ConnexionDB()
        return user
    else:
        return None
