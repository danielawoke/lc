from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .process_request import process_request

class load_applicant_info(APIView):
    def post(self, request, project_id, user_id, job_id):
        return process_request.post(request, project_id, user_id, job_id)