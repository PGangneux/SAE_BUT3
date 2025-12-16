from rest_framework.exceptions import APIException
from rest_framework import status


class ConnexionDB(APIException):
    def __init__(self):
        super().__init__(
            {"DataBase Connexion Failed": "Retry After"},
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )  # pragma: no cover
        self.status_code = status.HTTP_503_SERVICE_UNAVAILABLE  # pragma: no cover
