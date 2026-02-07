from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CSVImportJob

class CSVImportJobStatusView(APIView):
    """
    Endpoint pour récupérer le statut d'un job CSV.
    """

    def get(self, request, job_uuid, *args, **kwargs):
        try:
            job = CSVImportJob.nodes.get(uuid=job_uuid)
        except CSVImportJob.DoesNotExist:
            return Response({"error": "Job introuvable"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "uuid": job.uuid,
            "status": job.status,
            "message": job.message,
        })
