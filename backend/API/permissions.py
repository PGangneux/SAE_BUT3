from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import AnonymousUser

class IsAdminOrReadOnly(BasePermission):
    """
    Permet aux utilisateurs d'effectuer des requêtes 'GET', 'HEAD', 'OPTIONS'
    Nécessaire d'être administrateur dans le cas contraîre
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or type(request.user) != AnonymousUser
            and request.user.is_admin
        )


class IsAdmin(BasePermission):
    """
    Nécessite d'être administrateur
    """

    def has_permission(self, request, view):
        return bool(
            type(request.user) != AnonymousUser and request.user.is_admin
        )
