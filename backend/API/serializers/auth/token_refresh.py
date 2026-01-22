from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from backend.settings import SIMPLE_JWT as api_settings

from ...models import Utilisateur

class TokenRefresh(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        user_id = refresh.payload.get(api_settings.get("USER_ID_CLAIM"), None)
        if user_id:
            user = Utilisateur.nodes.get(uuid=user_id)

            # Pas encore pris en compte
            # if not api_settings.USER_AUTHENTICATION_RULE(user):
            #     raise AuthenticationFailed(
            #         self.error_messages["no_active_account"],
            #         "no_active_account",
            #     )

        data = {"access": str(refresh.access_token)}

        if api_settings.get("ROTATE_REFRESH_TOKENS"):
            if api_settings.get("BLACKLIST_AFTER_ROTATION"):
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
            refresh.outstand()

            data["refresh"] = str(refresh)

        return data
