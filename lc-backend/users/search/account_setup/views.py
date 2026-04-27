from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .process_request import process_request

class view(APIView):
    def get(self, request, user_id):
        return process_request.get(request, user_id)