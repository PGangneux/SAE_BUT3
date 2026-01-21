# views.py
import csv
import io

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import ArtisteSerializer, ThemeSerializer, QuestionSerializer, TagSerializer



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


        self.save_data(csv_file)

        return Response(
            {"message": "lignes importées avec succès"},
            status=status.HTTP_201_CREATED
        )
    

    def save_data(self, csv_file):
                # Lecture du fichier (UTF-8 recommandé)
        data = csv_file.read().decode("utf-8")
        io_string = io.StringIO(data)

        reader = csv.DictReader(io_string)

        for row in reader:
            print(row)  # Pour debug
            print(type(row))  # Pour debug
            self.save_row(row)





    def save_row(self, row):
        serializer_artiste = ArtisteSerializer()
        artiste  = row["Artiste"].strip() 
        if artiste != "" and artiste is not None:
            try:
                serializer_artiste.create({"name": artiste})
            except:
                pass

        serializer_theme = ThemeSerializer()
        theme  = row["Theme"].strip() 
        if theme != "" and theme is not None:
            try:
                serializer_theme.create({"name": theme})
            except:
                pass

        serializer_question = QuestionSerializer()
        question  = row["Question"].strip()
        if question != "" and question is not None:
            try:
                serializer_question.create({"text": question})
            except:
                pass
        
        serializer_tag = TagSerializer()
        tags = [tag.strip() for tag in row["Tags"].split("; ")]
        for tag in tags:
            if tag != "" and tag is not None:
                try:
                    serializer_tag.create({"name": tag})
                except:
                    pass

        
        




        #serializer_theme = Theme


        # return {
        #     "artiste": row["ARTISTE"].strip(),
        #     "theme": row["Thème"].strip(),
        #     "question": row["Question"].strip(),
        #     "tags": [tag.strip() for tag in row["Tags"].split(",")],
        #     "date": row["Date"].strip(),
        #     "evenement": row["Evénement"].strip(),
        #     "ville": row["Ville"].strip(),
        #     "youtube": row["YouTube"].strip(),
        #     "vimeo": row["Vimeo"].strip()
        # }