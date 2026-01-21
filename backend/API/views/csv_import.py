# views.py
import csv
import io

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CSVImportView(APIView):
    """
    Permet d'importer un fichier CSV contenant des extraits d'interviews.
    """

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get("file")

        if not csv_file:
            return Response(
                {"error": "Aucun fichier envoyé"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification basique
        if not csv_file.name.endswith(".csv"):
            return Response(
                {"error": "Le fichier doit être un CSV"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lecture du fichier (UTF-8 recommandé)
        data = csv_file.read().decode("utf-8")
        io_string = io.StringIO(data)

        reader = csv.DictReader(io_string)

        for row in reader:
            print(row)  # Pour debug
        return Response(
            {"message: lignes importées avec succès"},
            status=status.HTTP_201_CREATED
        )
