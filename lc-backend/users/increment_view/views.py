from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .process_request import process_request

class view(APIView):
    def post(self, request, entry_id):
        return process_request.post(entry_id)