from rest_framework.exceptions import ValidationError


class OrderError(ValidationError):
    """
    Le champ avec lequel l'order a été éxécuté n'est pas correct
    Il n'est pas possible d'order le nodeset avec ce champ
    """

    def __init__(self, order: str):
        super().__init__({"Order error": order})
