from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .process_request import process_request

class load_candidates(APIView):
    def get(self, request, project_id, user_id):
        return process_request.get(self, user_id, project_id)