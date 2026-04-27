from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .process_request import process_request

class load_applicant_info(APIView):
    def get(self, request, proposal_id):
        return process_request.get(request, proposal_id=proposal_id)