from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .process_request import process_request

class testView(APIView):
    def get(self, request, project_id, view_mode):
        return process_request.get(request, project_id=project_id, view_mode=view_mode)