from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Permet aux utilisateurs d'effectuer des requêtes 'GET', 'HEAD', 'OPTIONS'
    Nécessaire d'être administrateur dans le cas contraîre
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_admin
        )


class IsAdmin(BasePermission):
    """
    Nécessite d'être administrateur
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_admin
        )
